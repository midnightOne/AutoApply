from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Generic
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
import asyncio
import logging

# Generic type for agent input/output
T = TypeVar('T')

class AgentStatus(str, Enum):
    """Agent execution status"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AgentResult(BaseModel, Generic[T]):
    """Result of agent execution"""
    success: bool = Field(..., description="Whether the operation was successful")
    data: Optional[T] = Field(None, description="Result data")
    error: Optional[str] = Field(None, description="Error message if failed")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    execution_time: float = Field(0.0, description="Execution time in seconds")
    
    @classmethod
    def success_result(cls, data: T, metadata: Dict[str, Any] = None) -> 'AgentResult[T]':
        """Create a successful result"""
        return cls(
            success=True,
            data=data,
            metadata=metadata or {}
        )
        
    @classmethod
    def failure_result(cls, error: str, metadata: Dict[str, Any] = None) -> 'AgentResult[T]':
        """Create a failed result"""
        return cls(
            success=False,
            error=error,
            metadata=metadata or {}
        )

class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        self.name = name
        self.config = config or {}
        self.status = AgentStatus.IDLE
        self.logger = logging.getLogger(f"autoapply.agents.{name}")
        self.execution_history: List[Dict[str, Any]] = []
        
    @abstractmethod
    async def execute(self, input_data: Any) -> AgentResult:
        """Execute the agent's main functionality"""
        pass
        
    @abstractmethod
    def validate_input(self, input_data: Any) -> bool:
        """Validate input data"""
        pass
        
    async def run(self, input_data: Any) -> AgentResult:
        """Run the agent with proper error handling and status management"""
        start_time = datetime.now()
        
        try:
            # Validate input
            if not self.validate_input(input_data):
                return AgentResult.failure_result("Invalid input data")
                
            # Update status
            self.status = AgentStatus.RUNNING
            self.logger.info(f"Starting execution for agent: {self.name}")
            
            # Execute
            result = await self.execute(input_data)
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            result.execution_time = execution_time
            
            # Update status
            self.status = AgentStatus.COMPLETED if result.success else AgentStatus.FAILED
            
            # Log execution
            self._log_execution(input_data, result, execution_time)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Agent {self.name} failed with error: {str(e)}")
            self.status = AgentStatus.FAILED
            execution_time = (datetime.now() - start_time).total_seconds()
            
            result = AgentResult.failure_result(str(e))
            result.execution_time = execution_time
            
            self._log_execution(input_data, result, execution_time)
            return result
            
    def _log_execution(self, input_data: Any, result: AgentResult, execution_time: float):
        """Log execution details"""
        execution_record = {
            "timestamp": datetime.now().isoformat(),
            "input_summary": self._summarize_input(input_data),
            "success": result.success,
            "error": result.error,
            "execution_time": execution_time,
            "metadata": result.metadata
        }
        
        self.execution_history.append(execution_record)
        
        # Keep only last 100 executions
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-100:]
            
    def _summarize_input(self, input_data: Any) -> str:
        """Create a summary of input data for logging"""
        if isinstance(input_data, dict):
            return f"Dict with keys: {list(input_data.keys())}"
        elif isinstance(input_data, list):
            return f"List with {len(input_data)} items"
        elif hasattr(input_data, '__dict__'):
            return f"{type(input_data).__name__} object"
        else:
            return str(type(input_data).__name__)
            
    def get_status(self) -> AgentStatus:
        """Get current agent status"""
        return self.status
        
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get execution history"""
        return self.execution_history.copy()
        
    def reset(self):
        """Reset agent to idle state"""
        self.status = AgentStatus.IDLE
        
    def cancel(self):
        """Cancel current execution"""
        self.status = AgentStatus.CANCELLED
        
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
        
    def update_config(self, key: str, value: Any):
        """Update configuration value"""
        self.config[key] = value
        
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        if not self.execution_history:
            return {}
            
        successful_executions = [ex for ex in self.execution_history if ex['success']]
        failed_executions = [ex for ex in self.execution_history if not ex['success']]
        
        metrics = {
            "total_executions": len(self.execution_history),
            "successful_executions": len(successful_executions),
            "failed_executions": len(failed_executions),
            "success_rate": len(successful_executions) / len(self.execution_history) * 100,
            "average_execution_time": sum(ex['execution_time'] for ex in self.execution_history) / len(self.execution_history),
            "last_execution": self.execution_history[-1]['timestamp'] if self.execution_history else None
        }
        
        if successful_executions:
            metrics["average_successful_execution_time"] = sum(ex['execution_time'] for ex in successful_executions) / len(successful_executions)
            
        return metrics

class AsyncAgent(BaseAgent):
    """Base class for agents that support async operations"""
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        super().__init__(name, config)
        self._tasks: List[asyncio.Task] = []
        
    async def execute_parallel(self, tasks: List[Any]) -> List[AgentResult]:
        """Execute multiple tasks in parallel"""
        async def run_task(task_data):
            return await self.run(task_data)
            
        results = await asyncio.gather(*[run_task(task) for task in tasks], return_exceptions=True)
        
        # Convert exceptions to failed results
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                processed_results.append(AgentResult.failure_result(str(result)))
            else:
                processed_results.append(result)
                
        return processed_results
        
    async def cleanup(self):
        """Clean up any running tasks"""
        for task in self._tasks:
            if not task.done():
                task.cancel()
                
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)
            
        self._tasks.clear()

class ChainableAgent(BaseAgent):
    """Base class for agents that can be chained together"""
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        super().__init__(name, config)
        self.next_agent: Optional['ChainableAgent'] = None
        
    def chain(self, next_agent: 'ChainableAgent') -> 'ChainableAgent':
        """Chain this agent with the next one"""
        self.next_agent = next_agent
        return next_agent
        
    async def run_chain(self, input_data: Any) -> AgentResult:
        """Run this agent and pass result to next agent"""
        result = await self.run(input_data)
        
        if result.success and self.next_agent:
            return await self.next_agent.run_chain(result.data)
        else:
            return result 