# WhatsApp Chat Analyzer

The WhatsApp Chat Analyzer is a Python script that processes a WhatsApp chat export file to analyze messages between two specified individuals. It calculates various statistics such as total word count, top 10 active days, and average response time for each individual. The results are saved in Markdown files.

## Features

- Separates messages between two specified individuals
- Excludes messages containing specified phrases
- Calculates total word count for each individual
- Determines top 10 active days based on word count
- Calculates average response time for each individual (with and without trimming outliers)
- Saves the results in Markdown files

## Requirements

- Python 3.x
- `json` module
- `os` module
- `re` module
- `datetime` module
- `collections` module

## Usage

1. Export your WhatsApp chat history to a text file.
2. Create a configuration JSON file (`config.json`) with the following structure:

```json
{
  "whatsapp_export_path": "path/to/your/whatsapp/export/file.txt",
  "person1": "Name of Person 1",
  "person2": "Name of Person 2",
  "phrases_to_ignore": [
    "phrase1",
    "phrase2",
    "..."
  ]
}
```

3. Update the `config.json` file with the appropriate values:
   - `whatsapp_export_path`: Path to your WhatsApp chat export file
   - `person1`: Name of the first person to analyze
   - `person2`: Name of the second person to analyze
   - `phrases_to_ignore`: List of phrases to exclude from the analysis

4. Run the script:

```
python app.py
```

5. The script will process the chat file and generate Markdown files for each person in the `messages` directory.

## Output

The script generates two Markdown files, one for each person specified in the configuration. The files are saved in the `messages` directory with the naming format `{person1}_{person2}/{person}.md`.

Each Markdown file contains the following information:

- Total word count for the person
- Top 10 active days based on word count
- Average response time (with and without trimming outliers)
- List of messages sent by the person

## Configuration

The script uses a configuration JSON file (`config.json`) to specify the necessary parameters. The configuration file should have the following structure:

```json
{
  "whatsapp_export_path": "path/to/your/whatsapp/export/file.txt",
  "person1": "Name of Person 1",
  "person2": "Name of Person 2",
  "phrases_to_ignore": [
    "phrase1",
    "phrase2",
    "..."
  ]
}
```

- `whatsapp_export_path`: Path to your WhatsApp chat export file.
- `person1`: Name of the first person to analyze.
- `person2`: Name of the second person to analyze.
- `phrases_to_ignore`: List of phrases to exclude from the analysis.

Make sure to update the `config.json` file with the appropriate values before running the script.

## Contact

For any queries or assistance, please reach out to:

- **Name**: Charl Cronje
- **Email**: [charl@cronje.me](mailto:charl@cronje.me)
- **LinkedIn**: [https://www.linkedin.com/in/charlpcronje](https://www.linkedin.com/in/charlpcronje)