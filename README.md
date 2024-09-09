# Lab Notebook Copilot

Lab Notebook Copilot is an interactive Streamlit application designed to assist researchers in managing and analyzing experimental data. It provides a chat interface powered by GPT-4, allowing users to interact with their experimental workflows and generate structured outputs.

## Features

- Interactive chat interface for querying experiment details
- Workflow management with editable content
- Structured data generation from natural language descriptions
- Dynamic heatmap visualization for sample metadata
- Toggleable structured data generation
- Clipboard functionality for easy sharing of responses

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/nadimest/eln_copilot.git
   cd eln_copilot
   ```

2. Install Poetry:
   ```
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Install dependencies:
   ```
   poetry install
   ```

4. Set up your OpenAI API key:
   - Create a `.streamlit/secrets.toml` file
   - Add your API key:
     ```toml
     OPENAI_API_KEY = "your-api-key-here"
     ```

5. Run the Streamlit app:
   ```
   poetry run streamlit run app.py
   ```

## Usage

1. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

2. Use the sidebar to select a workflow and toggle structured data generation.

3. Interact with the chat interface to query experiment details and generate structured outputs.

4. View and edit workflow content using the sidebar expander.

5. Explore generated heatmaps and structured data in the main interface.

## Project Structure

- `app.py`: Main Streamlit application file
- `components.py`: Contains UI components and helper functions
- `models.py`: Pydantic models for structured data
- `llm_parser.py`: Functions for interacting with the OpenAI API
- `heatmap_visualizer.py`: Functions for creating heatmap visualizations
- `workflows/`: Directory containing markdown files for different workflows

## Dependencies

- Streamlit
- OpenAI
- Pandas
- Plotly
- Pydantic
- Pyperclip

All dependencies are managed using Poetry and specified in the `pyproject.toml` file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

To contribute to this project:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- OpenAI for providing the GPT-4 model
- Streamlit for the web application framework
- Plotly for interactive visualizations

## Contact

Nadim Saad - [@nadimest](https://github.com/nadimest)

Project Link: [https://github.com/nadimest/eln_copilot](https://github.com/nadimest/eln_copilot)