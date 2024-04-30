# OpenAI Chatbot with gpt-3.5-turbo model

This is a AI Mascot for UVU that uses OpenAI's GPT-3.5-turbo language model to generate responses to user's spoken input.

## Installation

1. Clone the repository: `git clone https://github.com/bkarras12/RoboticMascot.git`
2. Install the required packages: `pip install -r requirements.txt`
3. Set up an OpenAI API key by following the instructions [here](https://platform.openai.com/account/api-keys)
4. Add your API key to your environment to be used without hard coding in your API key. 
    Open Command Prompt: You can find it by searching "cmd" in the start menu.

    Set environment variable in the current session: To set the environment variable in the current session, use the command below, replacing your-api-key-here with your actual API key:
        setx OPENAI_API_KEY "your-api-key-here"
        This command will set the OPENAI_API_KEY environment variable for the current session.
    
    or you can add this key directly into your machines environmental variables to be permanently added to your device, rather adding it again every session. 
    Permanent setup: 
        
    To make the setup permanent, add the variable through the system properties as follows:
        Right-click on 'This PC' or 'My Computer' and select 'Properties'.
        Click on 'Advanced system settings'.
        Click the 'Environment Variables' button.
        In the 'System variables' section, click 'New...' and enter OPENAI_API_KEY as the variable name and your API key as the variable value.
        Verification: To verify the setup, reopen the command prompt and type the command below. It should display your API key: echo %OPENAI_API_KEY%

5. Set up a Google API key by navigating to the Google Cloud Console and create a service account.
        Step-by-Step Guide to Create a Google Cloud Service Account
    Log In to Google Cloud Console:

    Visit Google Cloud Console (https://console.cloud.google.com) and sign in with your Google account.
    Select or Create a Project:

    Once logged in, you’ll see the dashboard. At the top of the page, there’s a project selector (dropdown). Click it to either select an existing project or create a new one by clicking “New Project” and following the prompts.
    Navigate to IAM & Admin:

    After selecting your project, click on the navigation menu (three horizontal lines in the upper left corner of the screen, often referred to as the "hamburger" menu).
    Scroll down to “IAM & Admin”. Click on it to expand further options.
    Click on “Service Accounts”. This will take you to the service accounts page for your project.
    Create a Service Account:

    On the Service Accounts page, click “Create Service Account” at the top of the page.
    Enter a service account name and description. The name should be unique within the project. The description should help you identify the service account's purpose later.
    Click “Create”.
    Assign Roles:

    After clicking "Create", you will be prompted to assign roles to the service account. Search and select roles that best fit the permissions you want to grant. For using the Text-to-Speech API, you might consider roles like “Text-to-Speech User”.
    Click “Continue” once you've selected the necessary roles.
    Grant Users Access (Optional):

    You can add users or groups who can access this service account. This step is optional and can be skipped if you are the only one using it.
    Click “Done” to finish creating the service account.
    Create and Download JSON Key:

    After the service account is created, click on it in the list of service accounts.
    Go to the "Manage Keys" tab.
    Click “Add Key” and choose “Create new key”.
    Select “JSON” as the key type and click “Create”. The file will download automatically to your system.

## Usage

To start the chatbot, navigate to the 'backend' directory, and run `main.py` using Python 3 in the terminal:

    python main.py


The Mascot will run through it's initialization sequence, and then prompt the user to speak. After listening for 5 seconds, the AI will process the audio and output a response. 

To end the Mascot, say "quit" when prompted for a response.


## Acknowledgments

* This chatbot was inspired by the [OpenAI GPT-3 Playground](https://beta.openai.com/playground/)
* The GPT-3 model is provided by [OpenAI](https://openai.com/)
* The Text-To-Speech and Speech-To-Text models are provided by [Google](https://console.cloud.google.com)
