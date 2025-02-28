# Exo Pipe for OpenWebUI

This repository contains a custom pipe function for [OpenWebUI](https://github.com/open-webui/open-webui) that allows you to connect to a local [exo](https://github.com/exo-explore/exo) LLM cluster directly from the OpenWebUI interface.

## What is exo?

[Exo](https://github.com/exo-explore/exo) is an open-source AI clustering service that allows you to run large language models (LLMs) locally. It provides a ChatGPT-compatible API endpoint that can be used with various front-ends.

## What does this pipe do?

This pipe function allows OpenWebUI to communicate with a locally running exo instance, enabling you to:

- Chat with your local exo LLMs directly from the OpenWebUI interface
- Use all OpenWebUI features while running inference on your own hardware
- Keep your conversations private by running everything locally

## Installation

### Prerequisites

- A working [OpenWebUI](https://github.com/open-webui/open-webui) installation
- A running [exo](https://github.com/exo-explore/exo) instance with a ChatGPT-compatible endpoint

### Installation Steps

1. Download the `exo_pipe.py` file from this repository.

2. In OpenWebUI, navigate to **Settings > Functions**.

3. Click on **Add Function**.

4. Upload the `exo_pipe.py` file or paste its contents into the editor.

5. Click **Save**.

6. The "Exo LLM Pipe" should now appear in the dropdown list when creating a new chat.

## Configuration

The pipe comes with default settings that you can modify in the OpenWebUI interface:

1. Navigate to **Settings > Functions**.

2. Find "Exo LLM Pipe" in the list and click on the edit (pencil) icon.

3. You can modify the following settings:
   - `exo_endpoint`: The URL of your exo API endpoint (default: `http://192.168.64.1:52415/v1/chat/completions`)
   - `default_model`: The default model to use if none is specified (default: `llama-3.2-1b`)
   - `max_turns`: Maximum allowable conversation turns (default: `100`)
   - `enable_status_indicator`: Enable/disable status indicators (default: `true`)
   - `emit_interval`: Interval between status emissions in seconds (default: `2.0`)

4. Click **Save** to apply your changes.

## Usage

1. Create a new chat in OpenWebUI.

2. Select "Exo LLM Pipe" from the dropdown menu.

3. Start chatting! Your messages will be processed by your local exo instance.

## Troubleshooting

If you encounter issues:

- **Pipe not showing in dropdown**: Ensure the file was uploaded correctly and OpenWebUI was restarted.
- **Connection errors**: Verify your exo endpoint is running and accessible from OpenWebUI.
- **Error responses**: Check the exo logs for details on any processing errors.
- **Debug mode**: Set `self.debug = True` in the pipe code to enable detailed logging.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [OpenWebUI](https://github.com/open-webui/open-webui) for the amazing interface
- [Exo](https://github.com/exo-explore/exo) for making local LLM deployment easy
