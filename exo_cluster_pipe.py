"""
title: Exo Cluster LLM Pipe
author: Cary Brown
author_url: https://github.com/carybrown
version: 0.1.2

This function defines a pipe class in OpenWeb UI  that connects to a local exo cluster chatGPT compatiable endpoint.

Note:  Change endpoint to the URL for the exo API endpoint below to chatGPT compatiable endpoint URL provided when you run exo
"""

from typing import Optional, Callable, Awaitable
from pydantic import BaseModel, Field
import os
import time
import requests


class Pipe:
    class Valves(BaseModel):
        exo_endpoint: str = Field(
            default="http://localhost:52415/v1/chat/completions",
            description="URL for the exo API endpoint",
        )
        default_model: str = Field(
            default="llama-3.2-1b",
            description="Default model to use if none is specified",
        )
        emit_interval: float = Field(
            default=2.0, description="Interval in seconds between status emissions"
        )
        enable_status_indicator: bool = Field(
            default=True, description="Enable or disable status indicator emissions"
        )
        max_turns: int = Field(
            default=100, description="Maximum allowable conversation turns for a user"
        )

    def __init__(self):
        self.type = "pipe"
        self.id = "exo_pipe"
        self.name = "Exo LLM Pipe"
        self.valves = self.Valves()
        self.last_emit_time = 0
        self.debug = True
        pass

    def log(self, message):
        """Helper method for conditional logging"""
        if self.debug:
            print(f"[EXO CONNECTOR] {message}")

    async def emit_status(
        self,
        __event_emitter__: Callable[[dict], Awaitable[None]],
        level: str,
        message: str,
        done: bool,
    ):
        current_time = time.time()
        if (
            __event_emitter__
            and self.valves.enable_status_indicator
            and (
                current_time - self.last_emit_time >= self.valves.emit_interval or done
            )
        ):
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "status": "complete" if done else "in_progress",
                        "level": level,
                        "description": message,
                        "done": done,
                    },
                }
            )
            self.last_emit_time = current_time

    async def pipe(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __event_emitter__: Callable[[dict], Awaitable[None]] = None,
        __event_call__: Callable[[dict], Awaitable[dict]] = None,
    ) -> Optional[dict]:
        await self.emit_status(
            __event_emitter__, "info", "Connecting to exo LLM...", False
        )

        messages = body.get("messages", [])

        # Check conversation turn limits if needed
        if __user__ and len(messages) > self.valves.max_turns:
            await self.emit_status(
                __event_emitter__,
                "error",
                f"Conversation turn limit exceeded. Max turns: {self.valves.max_turns}",
                True,
            )
            return {
                "error": f"Conversation turn limit exceeded. Max turns: {self.valves.max_turns}"
            }

        # Verify messages are available
        if not messages:
            await self.emit_status(
                __event_emitter__,
                "error",
                "No messages found in the request body",
                True,
            )
            return {"error": "No messages found in the request body"}

        try:
            # Prepare request for exo API
            request_body = {
                "model": body.get("model") or self.valves.default_model,
                "messages": messages,
            }

            # Include any other parameters that might be relevant
            for param in [
                "temperature",
                "max_tokens",
                "top_p",
                "frequency_penalty",
                "presence_penalty",
            ]:
                if param in body:
                    request_body[param] = body[param]

            self.log(f"Sending request to exo endpoint: {self.valves.exo_endpoint}")
            await self.emit_status(
                __event_emitter__, "info", "Generating response with exo...", False
            )

            # Make the API call to exo endpoint
            response = requests.post(
                self.valves.exo_endpoint,
                json=request_body,
                headers={"Content-Type": "application/json"},
            )

            # Check if the request was successful
            response.raise_for_status()

            # Parse the JSON response
            exo_response = response.json()
            self.log(f"Successfully received response from exo")

            # Extract the assistant's message from the response
            try:
                assistant_message = exo_response["choices"][0]["message"]["content"]
                # Remove <|eot_id|> tag if present (specific to exo)
                assistant_message = assistant_message.replace("<|eot_id|>", "")

                # Add the assistant's response to the messages
                body["messages"].append(
                    {"role": "assistant", "content": assistant_message}
                )

                await self.emit_status(
                    __event_emitter__, "info", "Response generated successfully", True
                )
                return assistant_message

            except (KeyError, IndexError) as e:
                error_msg = f"Error parsing exo response: {str(e)}"
                self.log(f"ERROR: {error_msg}")
                await self.emit_status(__event_emitter__, "error", error_msg, True)
                return {"error": error_msg}

        except requests.exceptions.RequestException as e:
            # Handle any errors that might occur during the API call
            error_msg = f"Error calling exo API: {str(e)}"
            self.log(f"ERROR: {error_msg}")
            await self.emit_status(__event_emitter__, "error", error_msg, True)
            return {"error": error_msg}
