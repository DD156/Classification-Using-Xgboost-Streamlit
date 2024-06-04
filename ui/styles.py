style = """
<style>
/* Base styles */
html, body, .stApp {
    font-family: 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;
    background-color: #5A4E7C; /* A darker shade of purple for the background */
    color: #ffffff; /* White text for better contrast on dark background */
    margin: 0;
    padding: 0;
}
/* Header styles */
header {
    background-color: #67568C; /* Slightly lighter purple for the header */
    padding: 16px 40px; /* Adjusted padding */
    box-shadow: 0 2px 8px rgba(0,0,0,0.2); /* Darker shadow for depth */
    position: fixed;
    width: 100%;
    z-index: 999;
}

/* Navigation container styles */
.stButton > div {
    display: inline-block; /* Display the buttons inline */
}

/* Adjust the main content for fixed header */
main {
    padding-top: 80px; /* Header height adjustment */
}
/* Streamlit buttons */
button {
    border: none;
    border-radius: 5px; /* Rounded corners for buttons */
    padding: 10px 20px; /* Generous padding */
    margin: 0 10px; /* Space between buttons */
    transition: background-color 0.3s, box-shadow 0.3s;
}
/* Navigation button style */
button {
    background-color: transparent; /* Transparent background */
    color: #FFFFFF; /* White text */
    border: 1px solid #FFFFFF; /* White border */
}
button:hover {
    background-color: #7761A7; /* Lighter purple for hover */
    border: 1px solid #7761A7; /* Border color on hover */
}
/* Active page button style */
button:active {
    background-color: #4A3C5D; /* Even darker purple for the active button */
}
/* Footer styles */
footer {
    background-color: #67568C; /* Footer background matches the header */
    padding: 10px 0;
    position: fixed;
    bottom: 0;
    width: 100%;
    box-shadow: 0 -2px 8px rgba(0,0,0,0.2);
}
/* Main content styles */
.main-content {
    background-color: #7C71A1; /* Light purple background for content */
    border-radius: 8px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.3);
    padding: 20px;
    margin: 20px 40px; /* Adjusted margin */
}
/* Blog post container */
.blog-posts {
    display: flex; /* Flex container for side by side posts */
    justify-content: space-around; /* Space out the blog posts */
    flex-wrap: wrap; /* Wrap posts to next line on small screens */
}
/* Individual blog post styles */
.blog-post {
    background-color: #ffffff; /* White background for blog posts */
    color: #333333; /* Dark text for readability */
    border-radius: 8px;
    margin: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    transition: transform 0.3s;
    text-align: center; /* Center content within blog post */
}
.blog-post:hover {
    transform: translateY(-4px);
}
/* Blog post images */
.blog-post img {
    width: 100%; /* Force image to fill container */
    height: auto; /* Keep image aspect ratio */
    border-top-left-radius: 8px; /* Round the top corners of the image */
    border-top-right-radius: 8px;
}
/* Blog post links */
.blog-post a {
    display: block; /* Make the link fill the container */
    padding: 16px; /* Padding inside the link for space */
    color: #333333; /* Dark text */
    text-decoration: none; /* No underline */
}
/* Hover style for blog post links */
.blog-post a:hover {
    background-color: #EAEAEA; /* Light grey background for hover */
}
/* Adjust the footer for fixed header */
footer {
    padding-top: 10px;
}
/* Extra styles for smaller screens */
@media (max-width: 768px) {
    header {
        padding: 16px;
    }
    .main-content, footer {
        margin: 16px;
    }
    .blog-posts {
        flex-direction: column; /* Stack the blog posts on small screens */
    }
}
</style>
"""
  