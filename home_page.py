import streamlit as st


def home_page():

    # Hero Section with Columns
    st.markdown(
        """
        <h1 style='text-align: center; 
                    color: #007BFF; 
                    font-size: 2.5em; 
                    font-family: "Arial Black", sans-serif; 
                    text-shadow: 2px 2px 4px #000000;
                    padding-bottom: 10px;'>
            AI-Powered Web Scraping, PDF Data Extraction, Visualization & PDF QA Tool
        </h1>
        """,
        unsafe_allow_html=True
    )


    
        # Introduction for the African Centre for Statistics
    st.markdown(
        """
        <div style='text-align: center; 
                    padding: 15px; 
                    background-color: #e0f2f7; 
                    border-radius: 10px;
                    margin-bottom: 20px;'>
            <p style='font-size: 1.1em; line-height: 1.6;'>
                This AI-powered data analysis tool is developed in collaboration with the 
                <span style='font-weight: bold;'>African Centre for Statistics</span> 
                of the <span style='font-weight: bold;'>Economic Commission for Africa</span>. 
                It aims to enhance data accessibility, extraction, and analysis capabilities 
                for statistical offices and development stakeholders across Africa. 
                Our application empowers you to transform raw data into actionable intelligence using cutting-edge techniques.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown("---")

    # Feature Cards with Columns
    st.subheader("🚀 Core Features")
    cols = st.columns(4)
    features = [
        {"icon": "🌐", "title": "Web Scraping", "color": "#4CAF50",
         "desc": "Extract tables & files from any website"},
        {"icon": "📄", "title": "PDF Extraction", "color": "#2196F3",
         "desc": "Unlock hidden data in PDF documents"},
        {"icon": "📊", "title": "Data Viz", "color": "#9C27B0",
         "desc": "Interactive visualization & analysis"},
        {"icon": "🤖", "title": "PDF QA", "color": "#FF9800",
         "desc": "AI-powered document conversations"}
    ]

    for col, feature in zip(cols, features):
        with col:
            st.markdown(f"""
            <div style="border-left: 5px solid {feature['color']}; 
                        padding: 15px; 
                        margin: 10px 0;
                        border-radius: 5px;
                        background-color: #f8f9fa;">
                <h2 style="margin: 0; color: {feature['color']};">{feature['icon']} {feature['title']}</h2>
                <p>{feature['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    
    
    
    # Interactive Demo Section
    with st.expander("🎯 Quick Start Guide", expanded=True):
        st.markdown("""
        1. **Choose your tool** from the left navigation menu.
        2. **Follow the instructions** in each tool's page.
        3. **For detailed guidance**, visit the documentation page.
        4. **For support**, reach out to the developer team.
        """)
        st.button("🚀 Get Started Now", use_container_width=True)




    # Final CTA
    st.markdown("---")
    cta = st.container()
    cta.markdown("""
    <div style="text-align: center; padding: 30px; background-color: #e3f2fd; border-radius: 10px;">
        <h2>Ready to Transform Your Data Workflow?</h2>
        <p>Start your free exploration now!</p>
    </div>
    """, unsafe_allow_html=True)
    cta.button("✨ Begin Your Data Journey", type="primary", use_container_width=True)
