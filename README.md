# Quiz App (GUI Version)

A Python-based quiz application using Tkinter with multiple difficulty levels and timed questions.

## Features

- Three difficulty levels (Easy, Medium, Hard)
- 15-second timer for each question
- Progress tracking during the quiz
- Immediate feedback with score and percentage
- Clean, user-friendly interface
- Randomized question order

## Requirements

- Python 3.x
- Tkinter (usually comes with Python)
- CSV file with quiz questions

## Usage

1. Run the script: `python quiz_app.py`
2. Select your preferred difficulty level
3. Answer each question within the 15-second time limit
4. View your results at the end
5. Click "Restart Quiz" to play again

## File Structure

- `quiz_app.py` - Main application script
- `quiz_questions.csv` - Question database (must be in same directory)

## CSV File Format

The quiz questions CSV file must follow this format:
- difficulty,question,option1,option2,option3,option4,answer
- easy,What is the capital of France?,London,Paris,Rome,Berlin,Paris


## Customization

To add your own questions:
1. Edit the `quiz_questions.csv` file
2. Follow the same format as the existing questions
3. Save the file and restart the application

## Troubleshooting

- If you get a "File not found" error, ensure:
  - The CSV file is in the same directory as the script
  - The CSV file is named exactly `quiz_questions.csv`
  - You've downloaded the complete CSV file

- If the timer runs too fast:
  - This typically indicates a system performance issue
  - Try closing other applications while running the quiz

## 👨‍💻 Developed By

**Mohammad Amir Shoaib**  
💻 BCA Student | Front-End Web Developer  
📧 astechnical112@gmail.com  
🌐 [GitHub: @shoaibxbwf](https://github.com/shoaibxbwf)
PLS SUPPORT GIVE IT A STAR⭐⭐⭐⭐⭐
