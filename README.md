# Bible-Slide-Generator

Automate bilingual (Korean-English) Bible slide creation for ProPresenter using Python.

This tool imports Woori Bible (우리말성경), pairs it with ESV verses, and formats slides for worship services.

## Features

- Fetches Bible verses in both Korean and English.
- Generates PowerPoint slides with bilingual text.
- Customizable slide templates for different presentation styles.
- Supports creation of slides for any given book and chapter of the Bible.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher is installed on your system.
- Pip (Python package installer) is installed.
- Access to ESV API with a valid API key.

## Installation

To install Bible-Slide-Generator, follow these steps:

1. Clone the repository to your local machine:

`git clone https://github.com/your-username/Bible-Slide-Generator.git`

2. Navigate to the project directory:

`cd Bible-Slide-Generator`

3. Install the required Python packages:

`pip install -r requirements.txt`

## Usage

To generate Bible slides, perform the following:

1. Open the `bible_books.csv` file and enter the book names and chapter count for the Bible sections you wish to generate slides for.

2. Run the main script with the desired parameters (book name and chapter):

`python src/bible_slide_generator.py --book "Genesis" --chapter 1 --api-key "your_api_key"`

3. The slides will be generated in the `output` directory as a PowerPoint file.

## Customization

You can customize the slides by modifying the templates within the `templates` directory. Adjust fonts, colors, and layouts as needed.

## Contributos

- [Daniel Park](https://github.com/dannypark95)
- [Christina Song](https://github.com/christinasong97)

We welcome contributions and suggestions. Please open an issue or submit a pull request with your ideas.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

This project utilizes text from the Woori Bible and the ESV Bible, which are properties of their respective copyright holders.
