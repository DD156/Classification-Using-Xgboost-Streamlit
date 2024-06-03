import streamlit as st
from ui.styles import style
import pandas as pd 
from main_code.data_prep import make_prediction,plot_feature_importance,plot_gain
import streamlit.components.v1 as components


# Initialize session state for storing answers and results
if 'original_answers' not in st.session_state:
    st.session_state['original_answers'] = None
if 'new_answers' not in st.session_state:
    st.session_state['new_answers'] = None
if 'original_results' not in st.session_state:
    st.session_state['original_results'] = None
if 'new_results' not in st.session_state:
    st.session_state['new_results'] = None


def display_comparison(original_df, new_df):
    if original_df is not None and new_df is not None:
        # Reset indices
        original_df = original_df.reset_index(drop=True)
        new_df = new_df.reset_index(drop=True)

        # Create a mask DataFrame with the same shape as new_df
        mask = original_df.ne(new_df)

        # Convert mask of booleans into a mask of color styles
        mask = mask.replace({True: 'background-color: #ffcccb', False: ''})

        # Apply styling and display the dataframe
        st.dataframe(new_df.style.apply(lambda _: mask, axis=None))






def initialize_session_states():
    session_states = ['username', 'password', 'position', 'sidebar', 'current_page', 'is_logged_in']
    for state in session_states:
        if state not in st.session_state:
            st.session_state[state] = ''
            
            
initialize_session_states()

print(st.session_state)


if st.session_state['current_page'] == '':
                st.session_state['current_page'] = 'home'

def is_user_admin(username):
    # You should implement the actual check here
    return username == "admin"

def is_user_logged_in(username):
    print('hi')
    # Check if 'username' and 'password' are not empty in st.session_state
    if username != '' and st.session_state['password'] != '':
        if username != 'admin':
            st.session_state['position'] = 'student'
        st.session_state['is_logged_in'] = True
    else:
        st.session_state['is_logged_in'] = False
        st.session_state['position'] = ''
    print(st.session_state)
        
    
def handle_user_login():
    print('userLogin')
    if is_user_admin(st.session_state['username']) and st.session_state['is_logged_in'] == True:
        st.session_state['position'] = 'admin'
        st.session_state['is_logged_in'] = True
        show_admin_sidebar()
    elif st.session_state['is_logged_in'] == True:
        st.session_state['position'] = 'student'
        show_student_sidebar()
    else:
        print('pass happened')
        pass

def navigate_to(page_name):
    if page_name == "logout":
        logout()
        return
    st.session_state['current_page'] = page_name
    


def create_top_nav():
    menu_items = ["Be Buddy", "Profile", "Blog", "About Us", "FAQ"]
    menu_actions = ["home", "profile", "blog", "about-us", "faq"]

    if st.session_state['is_logged_in']:
        menu_items.append("Logout")
        menu_actions.append("logout")
    else:
        menu_items.append("Log in")
        menu_actions.append("login")
        menu_items.append("Register")
        menu_actions.append("register")

    col_nav = st.columns(len(menu_items),gap='small')
    for idx, menu_item in enumerate(menu_items):
        with col_nav[idx]:
            if st.button(menu_item, key=f'nav_{idx}'):
                if menu_actions[idx] == 'logout':
                    logout()
                else:
                    st.session_state['current_page'] = menu_actions[idx]
                            
def logout():
    st.session_state['username'] = ''
    st.session_state['password'] = ''
    st.session_state['is_logged_in'] = False
    st.session_state['current_page'] = 'home'  # Navigate to the home page
    
    
def show_profile_page():
    st.title("Profile")
    st.write("This is the profile page")
    

def show_login_page():
    with st.container():
        st.subheader("Login to your account")
        username = st.text_input("ID", placeholder="Enter your ID")
        print(username)
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        print(password)
        st.session_state['username'] = username
        st.session_state['password'] = password
        if st.button("Login", key='login'):
            st.success(f"Hello {username}, you're logged in!")
            st.session_state['current_page'] = 'home'
        if st.button("Create Account"):
            st.session_state['current_page'] = 'register'
            navigate_to("register")  # Navigate to the register page
    # Add this line to your main function or wherever you're handling page navigation
    
    
def upload_file():
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    if uploaded_file is not None:
        st.write(f"Test Results are being uploaded")
        df = pd.read_csv(uploaded_file)
        return df
    else:
        return None
        
    
def show_file_upload():
    upload_file()
    

    

    


def show_register_page():
    with st.container():
        st.subheader("Create a new account")
        new_username = st.text_input("Choose a ID", placeholder="New ID")
        new_password = st.text_input("Choose a password", type="password", placeholder="New password")
        confirm_password = st.text_input("Confirm password", type="password", placeholder="Confirm password")
        
        if new_password and confirm_password and new_password != confirm_password:
            st.error("Passwords do not match")
        if st.button("Register", key='register'):
            st.session_state['current_page'] = 'home'
            # Perform registration logic
            #st.success(f"Account created for {new_username}!")
            navigate_to("home")  # Redirect to home after registration
            
def show_faq_page():
    st.title("Frequently Asked Questions")
    st.markdown("""
                **1. How confidential are the test results, and who has access to them?**  
                *The test results are highly confidential. Access is limited to authorized personnel such as teachers and counselors, ensuring privacy and adherence to strict confidentiality standards.*

                **2. How does BeBuddy ensure the privacy of students taking the test?**  
                *BeBuddy employs advanced security methods to protect student privacy. Access to encrypted data is restricted to approved educators and counselors, safeguarding every student's privacy and well-being.*

                **3. Can students and parents access the test results directly?**  
                *No, test results are only accessible to authorized school personnel like teachers and counselors, maintaining a secure environment for student information.*

                **4. How frequently can teachers administer the test, and is it customizable?**  
                *Teachers can administer the test at the start of each semester, with flexibility in scheduling to meet unique educational needs.*

                **5. In what ways can teachers use BeBuddy to monitor students' well-being?**  
                *BeBuddy allows teachers to monitor student well-being efficiently. Quick access to confidential test results enables timely support for students in need.*

                **6. How does BeBuddy contribute to raising awareness about bullying?**  
                *BeBuddy is dedicated to raising bullying awareness by offering insightful test results and educational blog content, fostering understanding and a culture of kindness.*

                **7. How does BeBuddy's approach ensure a psychologically sound evaluation of students' well-being?**  
                *BeBuddy displays test results as percentages, providing a nuanced and accurate assessment that aligns with psychological health standards, endorsed by mental health professionals.*

                **8. How does BeBuddy support educators in addressing bullying in schools?**  
                *BeBuddy provides a swift and effective approach for educators to identify and address bullying, promoting a safer and more supportive learning environment.*

          """)

def show_about_page():
    st.title("About Us")

    # Using markdown for custom styling
    st.markdown("""
        <style>
            .subtitle {
                font-weight: 600;
                font-size: 22px;
                color: #264653; /* Deep greenish-blue color for subtitles */
                margin-bottom: 10px;
            }
            .content {
                color: #2a9d8f; /* Teal color for the text */
                font-size: 18px;
                margin-bottom: 20px;
            }
            img {
                border-radius: 8px;
                margin-top: 20px;
            }
        </style>
        """, unsafe_allow_html=True)

    # Splitting text into smaller paragraphs for readability
    st.markdown('<div class="subtitle">Welcome to BeBuddy</div>', unsafe_allow_html=True)
    st.markdown('<div class="content">where caring hearts and smart tech come together to make a real difference! Our goal is to establish a secure and encouraging environment for consultants, instructors, and students.</div>', unsafe_allow_html=True)
    
    
    
    
    
    st.markdown('<div class="subtitle">Our Mission</div>', unsafe_allow_html=True)
    st.markdown('<div class="content">The goal of our initiative is to provide teachers and consultants with the necessary tools to monitor and address bullying while also assisting students in understanding and navigating the school relationship.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="subtitle">Our Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="content">We\'ve created an inclusive platform with a group of driven individuals that not only recognises bullying but also encourages respect and kindness.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="subtitle">Join Our Community</div>', unsafe_allow_html=True)
    st.markdown('<div class="content">Come together with us as we create a community where everyone is free to thrive, grow, and learn.</div>', unsafe_allow_html=True)
    
    # Display images with captions
    col1, col2 = st.columns(2)
    with col1:
        st.image("imgs/photo4.jpg",use_column_width=True)
    with col2:
        st.image("imgs/photo2.jpg", use_column_width=True)

import pandas as pd
from datetime import datetime, date
import streamlit as st

def show_appointment_calendar():
    # Define the working hours
    HOURS = [(i, f"{i}:00 - {i+1}:00") for i in range(9, 18)]

    # Load or initialize booked slots
    try:
        booked_slots = pd.read_csv('booked_slots.csv')
        booked_slots['date'] = pd.to_datetime(booked_slots['date']).dt.date
    except FileNotFoundError:
        booked_slots = pd.DataFrame(columns=['date', 'hour'])

    # Streamlit UI
    st.title("Book an Appointment")
    date_selected = st.date_input("Choose a date", min_value=datetime.today().date())
    hour_selected = st.selectbox("Choose an hour", HOURS, format_func=lambda x: x[1])
    

        # If the slot is not booked, show a button to confirm the booking
    if st.button("Submit Booking"):
        if (date_selected, hour_selected[0]) in [(x['date'], x['hour']) for _, x in booked_slots.iterrows()]:
            print(booked_slots.values)
            st.error("This slot is already booked. Please choose another time.")
        else:
            # Book the slot
            booked_slots = booked_slots.append({'date': date_selected, 'hour': hour_selected[0]}, ignore_index=True)
            # Convert dates to string before saving to CSV
            booked_slots['date'] = booked_slots['date'].apply(
                lambda x: x.strftime('%Y-%m-%d') if isinstance(x, date) else x
            )
            booked_slots.to_csv('booked_slots.csv', index=False)
            st.success(f"Booked appointment on {date_selected} at {hour_selected[1]}")





            


              


def show_blog_page():
    st.title("Our Resources")

    # YouTube Section
    st.subheader("Videos")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("imgs/photo11.jpg", caption="Bullying Comes in All Shapes and Sizes")
    with col2:
        st.markdown("""
        **Bullying Comes in All Shapes and Sizes**: Bullying can happen to anyone, anywhere. Learn the signs and how to take action. 
        [Watch Video](https://youtu.be/JKYR9xxF_Hg?si=ltmlVAFB6RIED3Ed)
        """)
    
    col3, col4 = st.columns([1, 2])
    with col3:
        st.image("imgs/photo12.jpg", caption="Empower Yourself Against Bullying")
    with col4:
        st.markdown("""
        **Empower Yourself Against Bullying**: Gain the knowledge to handle bullying confidently. 
        [Watch Video](https://youtu.be/hiV3iCbzj4Y?si=Nbv5soGiJKOS-7gU)
        """)
    
    col5, col6 = st.columns([1, 2])
    with col5:
        st.image("imgs/photo13.jpg", caption="Young Anti-Bullying Alliance")
    with col6:
        st.markdown("""
        **Young Anti-Bullying Alliance**: Understand why it's important to support educators and caregivers. 
        [Watch Video](https://youtu.be/p9vheRqI54s?si=75NvL3sIzDqnrb6I)
        """)

    # Podcast Section
    st.subheader("Podcasts")

    col7, col8 = st.columns([1, 2])
    with col7:
        st.image("imgs/photo4.jpg", caption="Psychology Unplugged")
    with col8:
        st.markdown("""
        **Psychology Unplugged**: Delve into the complex relationships between bullying and social anxiety. 
        [Listen on Spotify](https://open.spotify.com/episode/0Tlvv9Bb9OEV2mqWQ90uPL?si=4QQL9KtZQb2lcWvwPkzi2g)
        """)
    
    col9, col10 = st.columns([1, 2])
    with col9:
        st.image("imgs/photo5.jpg", caption="Etacude Podcast")
    with col10:
        st.markdown("""
        **Etacude Podcast**: Discover strategies to deal with bullying at school. 
        [Listen on Spotify](https://open.spotify.com/episode/1GcCp0jXEZXx9Etip7u2GQ?si=sFwWeiDvT-O1E9Zt6cQaNA)
        """)
    
    col11, col12 = st.columns([1, 2])
    with col11:
        st.image("imgs/photo2.jpg", caption="Student's Life & Technology")
    with col12:
        st.markdown("""
        **Student's Life & Technology**: Explore the role of technology in education and its impact on students. 
        [Listen on Spotify](https://open.spotify.com/episode/2zVppgPTWtMm7HXeiCvC9O?si=OS_VVdb3SVm3F7YzQCbTwg)
        """)

    # Embedding custom styles for the blog page
    st.markdown("""
    <style>
    .blog-container {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        background: #f8f8ff; /* Light background for readability */
        color: #333; /* Darker text for readability */
        transition: box-shadow 0.3s ease-in-out;
    }
    .blog-container:hover {
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .blog-title {
        font-weight: bold;
        color: #333;
        margin-bottom: 15px;
    }
    .blog-text {
        color: #333;
    }
    .blog-link {
        color: #5d55fa; /* Adjusted for readability on light background */
        text-decoration: none;
        font-weight: bold;
    }
    .blog-link:hover {
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

    # Blog entry for the handbook
    st.markdown("""
    <div class="blog-container">
        <div class="blog-title">Preventing Violence and Bullying in Schools</div>
        <p class="blog-text">
            The Ministry of National Education (MEB) has released a powerful handbook on 
            'Preventing Violence and Bullying in Schools.' This comprehensive guide is a vital resource 
            for educators, parents, and students alike, offering valuable insights and strategies to 
            create safe, nurturing school environments. Explore the guide on our blog and become part 
            of the movement for an inclusive and bully-free learning environment!
        </p>
        <a class="blog-link" href="https://kraal.meb.k12.tr/meb_iys_dosyalar/06/06/974807/dosyalar/2015_04/20084157_okullardaiddetinnlenmesiogrenci_el_kitabi.pdf" target="_blank">Read the Handbook</a>
    </div>
    """, unsafe_allow_html=True)

    # Blog entry for the presentations
    st.markdown("""
    <div class="blog-container">
        <div class="blog-title">Understanding Peer Bullying</div>
        <p class="blog-text">
            Check out these priceless presentations about peer bullying for teachers, parents, 
            and students in elementary, middle, and high school, provided by The Ministry of National Education. 
            These thoughtfully produced resources seek to educate and empower, promoting a more secure and 
            welcoming learning environment.
        </p>
        <a class="blog-link" href="https://orgm.meb.gov.tr/www/akran-zorbaligi/icerik/2085" target="_blank">Access Presentations</a>
    </div>
    """, unsafe_allow_html=True)

# Run the show blog page function to display the content

def render_page():
    print(st.session_state)
    print("render")
    if st.session_state['current_page'] == 'Take the Test':
        take_the_test()
    elif st.session_state['current_page'] == 'Show Previous Tests':
        show_previous_tests()
    elif st.session_state['current_page'] == 'General Graphs':
        show_general_graphs()
    elif st.session_state['current_page'] == 'Sensitivity Analysis':
        show_sensitivity_analysis()
    elif st.session_state['current_page'] == 'What-if Analysis':
        show_what_if_analysis()
    elif st.session_state['current_page'] == 'File Upload':
        show_file_upload()
    elif st.session_state['current_page'] == 'Student Results':
        show_student_results()
    elif st.session_state['current_page'] == 'Appointment Booking':
        show_appointment_calendar()
    elif st.session_state['current_page'] == 'home':
        create_main_content()
        create_blog_section()
        create_faq_section()
    elif st.session_state['current_page'] == 'login':
        show_login_page()
    elif st.session_state['current_page'] == 'register':
        show_register_page()
    # Add this line to your main function or wherever you're handling page navigation
    elif st.session_state['current_page'] == 'faq':
        show_faq_page()
    elif st.session_state['current_page'] == 'about-us':
        show_about_page()
    elif st.session_state['current_page'] == 'blog':
        show_blog_page()
    elif st.session_state['current_page'] == 'profile':
        show_profile_page()
    
    
    
        

def create_main_content():
    # Main content with a call-to-action button
    st.markdown("<h2 style='text-align: center; color: black;'>Welcome to Be Buddy!</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: black;'>Take a moment to answer a few thoughtful questions, helping us create a supportive community where every voice is heard, and together, we foster kindness and respect.</p>", unsafe_allow_html=True)
    
    # Center button with markdown
    button_html = """
        <style>
            div.stButton { display: flex; margin-left: auto; margin-right: auto; }
        </style>
        <div style='text-align: center;'>
            <button class='stButton' onclick='location.href=\"javascript:void(0)\"'>Take the Test</button>
        </div>
    """
    st.markdown(button_html, unsafe_allow_html=True)
    
    # Handling button click
    if st.session_state.get('take_test_clicked'):
        st.write("Test started!")  # You can add logic here to start the test or redirect the user
        # Reset or further handle the state after starting the test
        st.session_state['take_test_clicked'] = False

    st.markdown("<p style='text-align: center; color: black;'>Average Test Duration: 5 minutes</p>", unsafe_allow_html=True)



def create_blog_section():
    st.title("Blog")

    # Define your blog entries here
    blog_entries = [
        {
            "image": "imgs/photo2.jpg",
            "title": "Bullying Comes in All Shapes and Sizes",
            "text": "Bullying can happen to anyone, anywhere. Learn the signs and how to take action.",
            "link": "https://youtu.be/JKYR9xxF_Hg?si=ltmlVAFB6RIED3Ed"
        },
        {
            "image": "imgs/photo4.jpg",
            "title": "Empower Yourself Against Bullying",
            "text": "Gain the knowledge to handle bullying confidently.",
            "link": "https://youtu.be/hiV3iCbzj4Y?si=Nbv5soGiJKOS-7gU"
        },
        {
            "image": "imgs/photo5.jpg",
            "title": "Young Anti-Bullying Alliance",
            "text": "Understand why it's important to support educators and caregivers.",
            "link": "https://youtu.be/p9vheRqI54s?si=75NvL3sIzDqnrb6I"
        }
    ]

    # Create rows for each blog entry
    for blog in blog_entries:
        with st.container():
            col1, col2 = st.columns([1, 2], gap="medium")
            with col1:
                # Ensure the image file exists at the path specified.
                # You can adjust width as needed to control the image size.
                st.image(blog['image'], width=200, caption=blog['title'])
            with col2:
                st.subheader(blog['title'])
                st.write(blog['text'])
                # Here we create a clickable link instead of a button.
                st.markdown(f"[Watch Video]({blog['link']})", unsafe_allow_html=True)


def create_faq_section():
    # Custom CSS to improve the FAQ section's appearance
    st.markdown("""
        <style>
            .faq-question {
                font-weight: bold;
                color: #0078ff;  /* You can change the color */
                margin-bottom: 5px;
                font-size: 1.1em; /* Increase the font size */
            }
            .faq-answer {
                margin-bottom: 10px; /* Add some space below the answer */
            }
        </style>
    """, unsafe_allow_html=True)

    # FAQ section
    st.markdown("## FAQ", unsafe_allow_html=True)
    faqs = [
        ("Is the test confidential?", "Yes, the test is completely confidential. Your responses will be securely stored and only used for the purpose of this test."),
        ("How much time does the test take?", "The test typically takes about 15-20 minutes to complete."),
        ("How do I change my answer?", "You can change your answer by simply clicking on a different option. Your latest selection will be considered as your final answer."),
        ("How do I book an appointment?", "You can book an appointment by contacting our support team via the 'Contact Us' page."),
        ("Can I take the test again?", "Yes, you can take the test as many times as you want. However, please note that only your most recent test results will be considered.")
    ]

    for question, answer in faqs:
        st.markdown(f"<div class='faq-question'>{question}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='faq-answer'>{answer}</div>", unsafe_allow_html=True)


    

st.markdown(style, unsafe_allow_html=True)

def update_csv(student_id,df,column_name,new_value):
    df.loc[df['STUDENT ID'] == student_id, column_name] = new_value
    df.to_csv('prediction.csv', index=False)
    
    
def load_data():
    return pd.read_csv('prediction.csv')

# Function to save the CSV file
def save_data(df):
    df.to_csv('prediction.csv', index=False)

# Function to update a student's test answers
def update_test(updates,index,student_id = st.session_state['username']):
    df = load_data()
    student_data = df[(df['Student ID'] == student_id) & (df.index == index)]
    print(student_data)
    print(updates)
    
    if not student_data.empty:
        for key, value in updates.items():
            df.loc[(df['Student ID'] == student_id) & (df.index == index), key] = value
            print(df)
        save_data(df)
        st.success('Test updated successfully.')
    else:
        st.error('Student ID not found.')

# Display each row as a separate dataframe
def show_previous_tests():
    df = pd.read_csv('prediction.csv')
    
    questions = {
    "Bullied_not_on_school_property_in_past_12_months": ["No", "Yes"],
    "Cyber_bullied_in_past_12_months": ["No", "Yes"],
    "Custom_Age": ["14 years old", "13 years old", "15 years old", "16 years old", "17 years old", "12 years old", "18 years old or older", "11 years old or younger"],
    "Sex": ["Male", "Female"],
    "Physically_attacked": ["0 time", "1 time", "4 or 5 times", "10 or 11 times", "2 or 3 times", "12 or more times", "6 or 7 times", "8 or 9 times"],
    "Physical_fighting": ["0 time", "1 time", "2 or 3 times", "8 or 9 times", "4 or 5 times", "6 or 7 times", "10 or 11 times", "12 or more times"],
    "Felt_lonely": ["Never", "Most of the time", "Rarely", "Sometimes", "Always"],
    "Close_friends": ["3 or more", "2", "0", "1"],
    "Miss_school_no_permission": ["0 days", "3 to 5 days", "10 or more days", "1 or 2 days", "6 to 9 days"],
    "Other_students_kind_and_helpful": ["Sometimes", "Most of the time", "Rarely", "Always", "Never"],
    "Parents_understand_problems": ["Always", "Sometimes", "Rarely", "Most of the time", "Never"],
    "Most_of_the_time_or_always_felt_lonely": ["No", "Yes"],
    "Missed_classes_or_school_without_permission": ["No", "Yes"],
    "Were_underweight": ["No", "Yes"],
    "Were_overweight": ["No", "Yes"],
    "Were_obese": ["No", "Yes"]
}
    
    question_mapping = {
        "Bullied_not_on_school_property_in_past_12_months": "Were you bullied(abuse,fighting,threat exc) outside of school property in the past 12 months?",
        "Cyber_bullied_in_past_12_months": "Have you been cyberbullied in past 12 months? ( like someone posting your embrassing photos or videos on social media, sending hurtful, threating messages, images or videos to you via messaging platform etc)",
        "Custom_Age": "What is your age group?",
        "Sex": "What is your gender?",
        "Physically_attacked": "How often have you been physically attacked?",
        "Physical_fighting": "How often have you been involved in physical fights?(an exchange of blows or one student assaulting another student )",
        "Felt_lonely": "How often do you feel lonely?",
        "Close_friends": "How many close friends do you have?",
        "Miss_school_no_permission": "How many days have you missed school without permission(like avoiding participating in school activities)?",
        "Other_students_kind_and_helpful": "How often do you think other students are kind and helpful to you?",
        "Parents_understand_problems": "How often do your parents understand your problems?",
        "Most_of_the_time_or_always_felt_lonely": "Do you feel lonely most of the time or always?",
        "Missed_classes_or_school_without_permission": "Have you missed classes or school without permission (like avoiding like avoiding participating in school activities)?",
        "Were_underweight": "Do you consider yourself underweight?",
        "Were_overweight": "Do you consider yourself overweight?",
        "Were_obese": "Do you think your weight is higher than what is considered healthy? Do you think you have an obesity disease?"
    }
    st.title("Update Test Answers")

    # Select a student ID
    df = load_data()

    # Display current answers for the student
    student_data = df[df['Student ID'] == st.session_state['username']]
    if not student_data.empty:
        st.subheader("Current Answers")
        st.dataframe(student_data)

        index_to_update = st.number_input("Enter the test_number to update")
        # Allow the user to select a question to update
        question_to_update = st.selectbox("Select a question to update", list(question_mapping.values()))

        # Find the corresponding column name for the selected question
        column_to_update = [key for key, value in question_mapping.items() if value == question_to_update][0]

        # Select a new answer for the question
        new_answer = st.selectbox("Select a new answer", questions[column_to_update])

        # Button to submit changes
        if st.button("Update Answer"):
            update_test({column_to_update: new_answer},index_to_update,st.session_state['username'])
    




def take_the_test():
    st.title("Welcome to the Test")
    st.write("Please answer all the questions below to the best of your ability.")

    # Define the questions and the possible answers
    questions = {
    "Bullied_not_on_school_property_in_past_12_months": ["No", "Yes"],
    "Cyber_bullied_in_past_12_months": ["No", "Yes"],
    "Custom_Age": ["14 years old", "13 years old", "15 years old", "16 years old", "17 years old", "12 years old", "18 years old or older", "11 years old or younger"],
    "Sex": ["Male", "Female"],
    "Physically_attacked": ["0 time", "1 time", "4 or 5 times", "10 or 11 times", "2 or 3 times", "12 or more times", "6 or 7 times", "8 or 9 times"],
    "Physical_fighting": ["0 time", "1 time", "2 or 3 times", "8 or 9 times", "4 or 5 times", "6 or 7 times", "10 or 11 times", "12 or more times"],
    "Felt_lonely": ["Never", "Most of the time", "Rarely", "Sometimes", "Always"],
    "Close_friends": ["3 or more", "2", "0", "1"],
    "Miss_school_no_permission": ["0 days", "3 to 5 days", "10 or more days", "1 or 2 days", "6 to 9 days"],
    "Other_students_kind_and_helpful": ["Sometimes", "Most of the time", "Rarely", "Always", "Never"],
    "Parents_understand_problems": ["Always", "Sometimes", "Rarely", "Most of the time", "Never"],
    "Most_of_the_time_or_always_felt_lonely": ["No", "Yes"],
    "Missed_classes_or_school_without_permission": ["No", "Yes"],
    "Were_underweight": ["No", "Yes"],
    "Were_overweight": ["No", "Yes"],
    "Were_obese": ["No", "Yes"]
}
    
    question_mapping = {
        "Bullied_not_on_school_property_in_past_12_months": "Were you bullied(abuse,fighting,threat exc) outside of school property in the past 12 months?",
        "Cyber_bullied_in_past_12_months": "Have you been cyberbullied in past 12 months? ( like someone posting your embrassing photos or videos on social media, sending hurtful, threating messages, images or videos to you via messaging platform etc)",
        "Custom_Age": "What is your age group?",
        "Sex": "What is your gender?",
        "Physically_attacked": "How often have you been physically attacked?",
        "Physical_fighting": "How often have you been involved in physical fights?(an exchange of blows or one student assaulting another student )",
        "Felt_lonely": "How often do you feel lonely?",
        "Close_friends": "How many close friends do you have?",
        "Miss_school_no_permission": "How many days have you missed school without permission(like avoiding participating in school activities)?",
        "Other_students_kind_and_helpful": "How often do you think other students are kind and helpful to you?",
        "Parents_understand_problems": "How often do your parents understand your problems?",
        "Most_of_the_time_or_always_felt_lonely": "Do you feel lonely most of the time or always?",
        "Missed_classes_or_school_without_permission": "Have you missed classes or school without permission (like avoiding like avoiding participating in school activities)?",
        "Were_underweight": "Do you consider yourself underweight?",
        "Were_overweight": "Do you consider yourself overweight?",
        "Were_obese": "Do you think your weight is higher than what is considered healthy? Do you think you have an obesity disease?"
    }
    

    # Initialize an empty dictionary to store the answers
    answers = {}
    student_id = st.number_input("Student ID", min_value=1, step=1)
    answers["Student ID"] = student_id
    
    for i,(key,friendly_question) in enumerate(question_mapping.items()):
        options = questions[key]
        answer = st.selectbox(friendly_question, options, key=f'question_{i}')
        answers[key] = answer
    
    print(f"Answers: {answers}")
    
    if st.button('Submit Answers'):
        # Convert the answers dictionary to a DataFrame
        result_df = make_prediction(answers)

        # Save the prediction to a CSV file
        result_df.to_csv('prediction.csv',mode='a',index=False)

        st.write("Thank you for taking the test!")
        
        navigate_to("home")  # Redirect to home after test completion
        #render_page()

# Define the functions to be called when each button is clicked
def show_general_graphs():
    # Code to display general graphs (e.g., PowerBI)
    # Write a code for generating a powerbi with a url
    # Your Power BI report URL
    power_bi_report_url = "powerbi url for your report"    
    
    # Embed the report using an iframe
    components.iframe(power_bi_report_url, width=1000, height=1000, scrolling=True)

def show_student_results():
    # Code to display general graphs (e.g., PowerBI)
    # Write a code for generating a powerbi with a url
    # Your Power BI report URL
    power_bi_report_url = "powerbi url for your report"    
    
    # Embed the report using an iframe
    components.iframe(power_bi_report_url, width=1500, height=1500, scrolling=True)
    

def show_sensitivity_analysis():
    st.title("Model Sensitivity Analysis")
    st.subheader("Feature Gain")
    fig_gain = plot_gain()
    st.pyplot(fig_gain)
    


def show_what_if_analysis():
    st.title("Welcome to the What-if Analysis")


    # Define the questions and the possible answers
    questions = {
    "Bullied_not_on_school_property_in_past_12_months": ["No", "Yes"],
    "Cyber_bullied_in_past_12_months": ["No", "Yes"],
    "Custom_Age": ["14 years old", "13 years old", "15 years old", "16 years old", "17 years old", "12 years old", "18 years old or older", "11 years old or younger"],
    "Sex": ["Male", "Female"],
    "Physically_attacked": ["0 time", "1 time", "4 or 5 times", "10 or 11 times", "2 or 3 times", "12 or more times", "6 or 7 times", "8 or 9 times"],
    "Physical_fighting": ["0 time", "1 time", "2 or 3 times", "8 or 9 times", "4 or 5 times", "6 or 7 times", "10 or 11 times", "12 or more times"],
    "Felt_lonely": ["Never", "Most of the time", "Rarely", "Sometimes", "Always"],
    "Close_friends": ["3 or more", "2", "0", "1"],
    "Miss_school_no_permission": ["0 days", "3 to 5 days", "10 or more days", "1 or 2 days", "6 to 9 days"],
    "Other_students_kind_and_helpful": ["Sometimes", "Most of the time", "Rarely", "Always", "Never"],
    "Parents_understand_problems": ["Always", "Sometimes", "Rarely", "Most of the time", "Never"],
    "Most_of_the_time_or_always_felt_lonely": ["No", "Yes"],
    "Missed_classes_or_school_without_permission": ["No", "Yes"],
    "Were_underweight": ["No", "Yes"],
    "Were_overweight": ["No", "Yes"],
    "Were_obese": ["No", "Yes"]
}
    
    question_mapping = {
        "Bullied_not_on_school_property_in_past_12_months": "Were you bullied(abuse,fighting,threat exc) outside of school property in the past 12 months?",
        "Cyber_bullied_in_past_12_months": "Have you been cyberbullied in past 12 months? ( like someone posting your embrassing photos or videos on social media, sending hurtful, threating messages, images or videos to you via messaging platform etc)",
        "Custom_Age": "What is your age group?",    
        "Sex": "What is your gender?",
        "Physically_attacked": "How often have you been physically attacked?",
        "Physical_fighting": "How often have you been involved in physical fights?(an exchange of blows or one student assaulting another student )",
        "Felt_lonely": "How often do you feel lonely?",
        "Close_friends": "How many close friends do you have?",
        "Miss_school_no_permission": "How many days have you missed school without permission(like avoiding participating in school activities)?",
        "Other_students_kind_and_helpful": "How often do you think other students are kind and helpful to you?",
        "Parents_understand_problems": "How often do your parents understand your problems?",
        "Most_of_the_time_or_always_felt_lonely": "Do you feel lonely most of the time or always?",
        "Missed_classes_or_school_without_permission": "Have you missed classes or school without permission (like avoiding like avoiding participating in school activities)?",
        "Were_underweight": "Do you consider yourself underweight?",
        "Were_overweight": "Do you consider yourself overweight?",
        "Were_obese": "Do you think your weight is higher than what is considered healthy? Do you think you have an obesity disease?"
    }
    def capture_and_predict():
        answers = {}
        for key, friendly_question in question_mapping.items():
            answers[key] = st.session_state[key]
        result_df = make_prediction(answers)
        return result_df

    # Get new answers and make predictions
    st.subheader("What-if Analysis")
    for key, friendly_question in question_mapping.items():
        options = questions[key]
        st.selectbox(friendly_question, options, key=key)
    if st.button('Run What-if Analysis'):
        new_answers = {key: st.session_state[key] for key in question_mapping}
        new_results_df = capture_and_predict()
        if st.session_state['original_answers'] is None:
            st.session_state['original_answers'] = new_answers
            st.session_state['original_results'] = new_results_df
        else:
            if st.session_state['original_results'] is not None:
                st.subheader("Original Results")
                st.dataframe(st.session_state['original_results'])
                st.write(f"Machine learn decision on bullied :  {st.session_state['original_results']['Bullied_on_school_property_in_past_12_months'].values[0]}")
                st.write("Student is not bullied",icon=':smile:')
                
            st.session_state['new_answers'] = new_answers
            st.subheader("New Results")
            print("lasdlasdl")
            print(st.session_state['original_results'])
            print(new_results_df)
            print(st.session_state['original_answers'])
            print(st.session_state['new_answers'])
            st.session_state['original_results'].to_csv('prediction1.csv',mode='a',index=False)
            new_results_df.to_csv('prediction1.csv',mode='a',index=False)
            display_comparison(
                st.session_state['original_results'],
                new_results_df,
            )
            st.write(f"Machine learn decision on bullied :  {new_results_df['Bullied_on_school_property_in_past_12_months'].values[0]}")
            st.write("Student is to be bullied",icon=':cry:')



def show_student_sidebar():
    
    st.sidebar.title("Student Navigation")
    
    # Define a dictionary mapping button names to their respective functions
    buttons = {
        "Take the Test": take_the_test,
        "Show Previous Tests": show_previous_tests,
        "Appointment Booking":show_appointment_calendar
        # Add more buttons here...
    }
    
    # Loop over the buttons dictionary
    for i, (button_name, button_function) in enumerate(buttons.items()):
        print(button_name)
        if st.sidebar.button(button_name, key=f'student_{i}'):
            st.session_state['current_page'] = button_name
            #button_function()  # Call the function associated with the button

def show_admin_sidebar():
    st.sidebar.title("Admin Navigation")

    # Define a dictionary mapping button names to their respective functions
    buttons = {
        "General Graphs": show_general_graphs,
        "Sensitivity Analysis": show_sensitivity_analysis,
        "What-if Analysis": show_what_if_analysis,
        "Student Results": show_student_results,
        "File Upload": show_file_upload
        
        # Add more buttons here...
    }

    # Loop over the buttons dictionary
    for i, (button_name, button_function) in enumerate(buttons.items()):
        if st.sidebar.button(button_name, key=f'admin_{i}'):
            st.session_state['current_page'] = button_name
            #button_function()  # Call the function associated with the button


is_user_logged_in(st.session_state['username'])
handle_user_login()

# Use Streamlit components to create the UI
create_top_nav()
render_page()
