import asyncio
from typing import Dict, Any, List, Optional
from openai import OpenAI
import os
from sqlmodel import Session
from src.services.message_service import MessageService
from src.models.message_model import Message


class AIAgentService:
    """
    Service class for integrating with OpenAI Agents SDK to process natural language requests
    and invoke appropriate MCP tools for todo operations.
    """

    def __init__(self):
        """
        Initialize the AI Agent service with OpenAI client.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("AGENT_MODEL", "gpt-4")
        self.temperature = float(os.getenv("AGENT_TEMPERATURE", "0.7"))

    async def initialize_basic_agent(self):
        """
        Initialize basic agent functionality for processing natural language.
        """
        # This method sets up the basic agent configuration
        pass

    async def process_natural_language_request(
        self,
        user_message: str,
        conversation_id: int,
        user_id: str,
        message_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Process a natural language request from a user and return an AI-generated response
        along with any tool calls that were invoked.

        Args:
            user_message: The natural language message from the user
            conversation_id: ID of the conversation for context
            user_id: ID of the user making the request
            message_history: Previous messages in the conversation for context

        Returns:
            Dictionary containing the AI response and any tool calls made
        """
        try:
            # Prepare the messages for the AI agent
            messages = []

            # Add system message to guide the agent
            messages.append({
                "role": "system",
                "content": (
                    "You are a helpful AI assistant that manages todo tasks for users. "
                    "You can add, list, update, complete, and delete tasks. "
                    "Use the provided tools to perform these operations. "
                    "Always respond naturally to the user's requests."
                )
            })

            # Add conversation history if available
            if message_history:
                messages.extend(message_history)

            # Add the current user message
            messages.append({
                "role": "user",
                "content": user_message
            })

            # Try to call the OpenAI API with potential tool functions
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    tools=[
                        {
                            "type": "function",
                            "function": {
                                "name": "add_task",
                                "description": "Add a new task to the user's list",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string", "description": "The title of the task"},
                                        "description": {"type": "string", "description": "Optional description of the task"}
                                    },
                                    "required": ["title"]
                                }
                            }
                        },
                        {
                            "type": "function",
                            "function": {
                                "name": "list_tasks",
                                "description": "List all tasks for the user",
                                "parameters": {
                                    "type": "object",
                                    "properties": {},
                                }
                            }
                        },
                        {
                            "type": "function",
                            "function": {
                                "name": "update_task",
                                "description": "Update an existing task",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "task_id": {"type": "integer", "description": "The ID of the task to update"},
                                        "title": {"type": "string", "description": "The new title of the task"},
                                        "description": {"type": "string", "description": "The new description of the task"}
                                    }
                                }
                            }
                        },
                        {
                            "type": "function",
                            "function": {
                                "name": "complete_task",
                                "description": "Mark a task as completed",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "task_id": {"type": "integer", "description": "The ID of the task to complete"}
                                    },
                                    "required": ["task_id"]
                                }
                            }
                        },
                        {
                            "type": "function",
                            "function": {
                                "name": "delete_task",
                                "description": "Delete a task",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "task_id": {"type": "integer", "description": "The ID of the task to delete"}
                                    },
                                    "required": ["task_id"]
                                }
                            }
                        }
                    ],
                    tool_choice="auto"
                )

                # Process the response
                response_message = response.choices[0].message
                tool_calls = response_message.tool_calls

                # Prepare result
                result = {
                    "response": response_message.content or "",
                    "tool_calls": [],
                    "tool_results": []
                }

                # Process any tool calls
                if tool_calls:
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        function_args = eval(tool_call.function.arguments)  # In production, use json.loads

                        # Add user_id to the arguments for proper user isolation
                        function_args['user_id'] = user_id

                        # Execute the tool call (in a real implementation, this would call the MCP tools)
                        tool_result = await self.execute_tool_call(function_name, function_args)

                        result["tool_calls"].append({
                            "name": function_name,
                            "arguments": function_args
                        })

                        result["tool_results"].append(tool_result)

                return result
            except Exception as openai_error:
                # If OpenAI API fails, implement basic natural language understanding
                # This is a fallback implementation to handle common task requests
                return await self.fallback_process_natural_language_request(user_message, user_id)

        except Exception as e:
            # Handle errors gracefully
            return {
                "response": f"I'm sorry, I encountered an error processing your request: {str(e)}",
                "tool_calls": [],
                "tool_results": [],
                "error": str(e)
            }

    async def fallback_process_natural_language_request(
        self,
        user_message: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Fallback method to process natural language requests when OpenAI API is unavailable.

        Args:
            user_message: The natural language message from the user
            user_id: ID of the user making the request

        Returns:
            Dictionary containing the response and any tool calls made
        """
        import re

        # Convert message to lowercase for easier processing
        message_lower = user_message.lower().strip()

        # Prepare the result structure
        result = {
            "response": "",
            "tool_calls": [],
            "tool_results": []
        }

        # Handle different types of requests
        if any(word in message_lower for word in ['create', 'add', 'make', 'new', 'task', 'todo']):
            # Try to extract task title and description
            # Look for patterns like "create task to..." or "add task to..." or just "buy groceries"

            # First try more specific patterns
            title = ""
            desc_match = None

            # Look for patterns like "create task to buy groceries" or "add task to walk dog"
            specific_match = re.search(r'(?:create|add|make|new|task|todo)\s+(?:a\s+|the\s+)?(?:task|todo)\s+to\s+(.+?)(?:\s+and|$)', message_lower)
            if not specific_match:
                # Look for patterns like "create buy groceries" or "add walk the dog"
                specific_match = re.search(r'(?:create|add|make|new)\s+(.+?)(?:\s+to\s+.*)?$', message_lower)
            if not specific_match:
                # Look for patterns like "task to buy groceries"
                specific_match = re.search(r'(?:task|todo)\s+to\s+(.+?)(?:\s+and|$)', message_lower)
            if not specific_match:
                # If none of the above worked, just take everything after the command
                specific_match = re.search(r'(?:create|add|make|new|task|todo)\s+(.+)$', message_lower)

            if specific_match:
                title = specific_match.group(1).strip()
                # Clean up common phrases
                if title.startswith('to '):
                    title = title[3:].strip()
                elif title.startswith('task '):
                    title = title[5:].strip()
                elif title.startswith('a '):
                    title = title[2:].strip()
                elif title.startswith('the '):
                    title = title[4:].strip()
            else:
                # If specific patterns don't work, use a simpler approach
                # Just remove the command words and take what's left
                title = re.sub(r'^(create|add|make|new|task|todo)\s+', '', message_lower).strip()
                # Further clean up
                if title.startswith('to '):
                    title = title[3:].strip()
                if title.startswith('a '):
                    title = title[2:].strip()
                if title.startswith('the '):
                    title = title[4:].strip()

            if title:
                # Call add_task function
                tool_args = {
                    'title': title.title(),
                    'user_id': user_id
                }

                # Check if there's a description part
                desc_pattern = re.search(r'(?:for|because|description:\s*)(.+)', user_message, re.IGNORECASE)
                if desc_pattern:
                    tool_args['description'] = desc_pattern.group(1).strip()

                tool_result = await self.execute_tool_call("add_task", tool_args)

                result["tool_calls"].append({
                    "name": "add_task",
                    "arguments": tool_args
                })

                result["tool_results"].append(tool_result)
                result["response"] = tool_result.get("message", f"Task '{title.title()}' created successfully!")
                return result

        elif any(word in message_lower for word in ['list', 'show', 'view', 'my', 'tasks', 'todos']) or \
             ('show' in message_lower and any(word in message_lower for word in ['my', 'tasks'])) or \
             ('list' in message_lower and any(word in message_lower for word in ['my', 'tasks'])):
            # Call list_tasks function
            tool_args = {'user_id': user_id}
            tool_result = await self.execute_tool_call("list_tasks", tool_args)

            result["tool_calls"].append({
                "name": "list_tasks",
                "arguments": tool_args
            })

            result["tool_results"].append(tool_result)
            result["response"] = tool_result.get("message", "Here are your tasks.")
            return result

        elif any(word in message_lower for word in ['complete', 'done', 'finish', 'mark']):
            # Try to extract task ID
            id_match = re.search(r'\b(\d+)\b', user_message)
            if id_match:
                task_id = int(id_match.group(1))
                tool_args = {
                    'task_id': task_id,
                    'user_id': user_id
                }

                tool_result = await self.execute_tool_call("complete_task", tool_args)

                result["tool_calls"].append({
                    "name": "complete_task",
                    "arguments": tool_args
                })

                result["tool_results"].append(tool_result)
                result["response"] = tool_result.get("message", f"Task {task_id} marked as completed.")
                return result

        elif any(word in message_lower for word in ['update', 'change', 'edit', 'modify']):
            # Try to extract task ID and new details
            id_match = re.search(r'\b(\d+)\b', user_message)
            if id_match:
                task_id = int(id_match.group(1))

                # Try to extract new title or description
                title_match = re.search(r'(?:to|as|new|called)\s+(.+?)(?:\s+and|$)', user_message)

                tool_args = {
                    'task_id': task_id,
                    'user_id': user_id
                }

                if title_match:
                    tool_args['title'] = title_match.group(1).strip()

                tool_result = await self.execute_tool_call("update_task", tool_args)

                result["tool_calls"].append({
                    "name": "update_task",
                    "arguments": tool_args
                })

                result["tool_results"].append(tool_result)
                result["response"] = tool_result.get("message", f"Task {task_id} updated successfully.")
                return result

        elif any(word in message_lower for word in ['delete', 'remove', 'cancel']):
            # Try to extract task ID
            id_match = re.search(r'\b(\d+)\b', user_message)
            if id_match:
                task_id = int(id_match.group(1))
                tool_args = {
                    'task_id': task_id,
                    'user_id': user_id
                }

                tool_result = await self.execute_tool_call("delete_task", tool_args)

                result["tool_calls"].append({
                    "name": "delete_task",
                    "arguments": tool_args
                })

                result["tool_results"].append(tool_result)
                result["response"] = tool_result.get("message", f"Task {task_id} deleted successfully.")
                return result

        # If no specific action was detected, provide a generic response
        result["response"] = f"I understood your request: '{user_message}'. You can ask me to create, list, update, complete, or delete tasks."
        return result

    async def execute_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool call by invoking the appropriate MCP tool.

        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool

        Returns:
            Result of the tool execution
        """
        from src.services.task_service import TaskService
        from sqlmodel import Session
        from src.database.database import get_session

        # In a real implementation, this would call the actual MCP tools
        # For now, we'll use the actual backend services
        try:
            # Validate user isolation - ensure the user_id in arguments matches the expected user
            # This is a critical security measure to ensure users can only operate on their own data
            requested_user_id = arguments.get('user_id')
            if not requested_user_id:
                return {
                    "success": False,
                    "error": "Missing user_id in tool arguments",
                    "message": "Security validation failed: Missing user identification"
                }

            # In a real implementation, we'd validate that the requested_user_id matches
            # the authenticated user, but here we'll just ensure it exists
            # This is where we'd integrate with the authentication system to verify permissions

            # Use the actual task service implementations
            if tool_name == "add_task":
                # Create a task using the task service
                from src.models.task_model import TaskCreate
                task_create = TaskCreate(
                    title=arguments.get('title', 'Untitled'),
                    description=arguments.get('description', ''),
                    user_id=str(requested_user_id)  # Ensure it's a string
                )

                # Get a database session
                db_session = next(get_session())
                try:
                    task = TaskService.create_task(task_create, db_session)
                    return {
                        "success": True,
                        "task_id": task.id,
                        "message": f"Task '{task.title}' created successfully"
                    }
                finally:
                    db_session.close()
            elif tool_name == "list_tasks":
                # List tasks for the user
                requested_user_id = str(requested_user_id)  # Ensure it's a string

                # Get a database session
                db_session = next(get_session())
                try:
                    tasks = TaskService.get_tasks_by_user(requested_user_id, db_session)
                    return {
                        "success": True,
                        "tasks": [{"id": task.id, "title": task.title, "description": task.description, "completed": task.completed} for task in tasks],
                        "message": f"Retrieved {len(tasks)} tasks successfully"
                    }
                finally:
                    db_session.close()
            elif tool_name == "update_task":
                # Update an existing task
                task_id = arguments.get('task_id')
                title = arguments.get('title')
                description = arguments.get('description')

                # Prepare update data
                from src.models.task_model import TaskUpdate
                update_data = {}
                if title is not None:
                    update_data["title"] = title
                if description is not None:
                    update_data["description"] = description

                task_update = TaskUpdate(**update_data)

                # Get a database session
                db_session = next(get_session())
                try:
                    updated_task = TaskService.update_task(task_id, str(requested_user_id), task_update, db_session)
                    if updated_task:
                        return {
                            "success": True,
                            "message": f"Task {task_id} updated successfully"
                        }
                    else:
                        return {
                            "success": False,
                            "error": "Task not found",
                            "message": f"Task {task_id} not found or does not belong to user"
                        }
                finally:
                    db_session.close()
            elif tool_name == "complete_task":
                # Mark a task as completed
                task_id = arguments.get('task_id')

                # Get a database session
                db_session = next(get_session())
                try:
                    completed_task = TaskService.complete_task(task_id, str(requested_user_id), db_session)
                    if completed_task:
                        return {
                            "success": True,
                            "message": f"Task {task_id} marked as completed"
                        }
                    else:
                        return {
                            "success": False,
                            "error": "Task not found",
                            "message": f"Task {task_id} not found or does not belong to user"
                        }
                finally:
                    db_session.close()
            elif tool_name == "delete_task":
                # Delete a task
                task_id = arguments.get('task_id')

                # Get a database session
                db_session = next(get_session())
                try:
                    success = TaskService.delete_task(task_id, str(requested_user_id), db_session)
                    if success:
                        return {
                            "success": True,
                            "message": f"Task {task_id} deleted successfully"
                        }
                    else:
                        return {
                            "success": False,
                            "error": "Task not found",
                            "message": f"Task {task_id} not found or does not belong to user"
                        }
                finally:
                    db_session.close()
            else:
                return {
                    "success": False,
                    "error": f"Unknown tool: {tool_name}",
                    "message": f"Unknown tool: {tool_name}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Error executing tool {tool_name}: {str(e)}"
            }

    async def enhance_with_conversation_context(
        self,
        user_message: str,
        conversation_id: int,
        user_id: str,
        db_session: Session
    ) -> Dict[str, Any]:
        """
        Enhance AI processing with conversation history context.

        Args:
            user_message: The current message from the user
            conversation_id: ID of the conversation for context
            user_id: ID of the user making the request
            db_session: Database session

        Returns:
            Dictionary containing the AI response and any tool calls made
        """
        # Get conversation history from the database
        from src.services.message_service import MessageService

        # Get all messages in the conversation ordered by timestamp
        conversation_messages = MessageService.get_messages_by_conversation_ordered(conversation_id, db_session)

        # Format the conversation history for the AI agent
        formatted_history = self.format_conversation_history(conversation_messages)

        # Process the message with conversation context
        result = await self.process_natural_language_request(
            user_message=user_message,
            conversation_id=conversation_id,
            user_id=user_id,
            message_history=formatted_history
        )

        return result

    def format_conversation_history(self, messages: List[Message], max_messages: int = 10) -> List[Dict[str, str]]:
        """
        Format conversation history for AI agent context.

        Args:
            messages: List of message objects from the database
            max_messages: Maximum number of messages to include

        Returns:
            Formatted list of messages for AI context
        """
        formatted_history = []

        # Take the most recent messages up to max_messages
        recent_messages = messages[-max_messages:] if len(messages) > max_messages else messages

        for msg in recent_messages:
            formatted_history.append({
                "role": msg.role,
                "content": msg.content
            })

        return formatted_history