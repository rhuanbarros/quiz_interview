# 📚 Machine Learning Interview Preparation Trainer

## 🚀 Problem Addressed
I needed to study some topics in machine learning, but I couldn't find any specific quiz about them. 

Additionally, I wanted to keep track of the contents I studied and how many questions I got right and wrong. Therefore, I needed a custom UI interface and fine-grained questions.

## 💡 Solution
I could just ask ChatGPT to create the questions, but it got very repetitive. I realized that if I prompted it with a piece of text about the subject matter, it would create much better questions. So, I created a very customized prompt for this task.

The UI has some custom details:
- When I don't know the answer, I can click a button, and it automatically queries the Gemini model to explain the topic for me. This way, I don't need to leave the app and can continue the study session seamlessly. I used Streamlit to create the UI.
- I also wanted to keep track of my results over time, so I needed a backend. To solve this, I used the Supabase backend as a service platform. It offers a free online database that I could connect using Python.

Finally, I hosted the Streamlit UI in the cloud, allowing me to use the app even on my mobile phone.

## Key Points
- 📈 **Enhanced Learning**: Customized prompt generation for better question creation.
- 📚 **Integrated Knowledge**: Query Gemini model directly for explanations without leaving the app.
- 🗂️ **Result Tracking**: Keep track of study progress and quiz results over time.
- ☁️ **Cloud Accessibility**: Hosted in the cloud for access on mobile devices.

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/rhuanbarros/quiz_interview.git
   ```

2. Install dependencies
   ```bash
    poetry install --no-root
   ```
3. Run
   ```bash
    poetry run streamlit run ./src/main.py
   ```

## Publish to cloud
    - go to https://share.streamlit.io/
    - click in reboot. it will fetch the latest version from github.
    - if there is any change in apy key or dependencies, I think it should be updated in settings.