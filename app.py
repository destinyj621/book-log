import streamlit as st
import pandas as pd

# Function to load data from Excel file
def load_data(file_path):
    try:
        data = pd.read_excel(file_path)
        return data
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Function to save data to Excel file
def save_data(data, file_path):
    try:
        data.to_excel(file_path, index=False)
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

# Main function to run the app
def main():
    st.title("Book Tracker")

    # Load data
    file_path = "BookLog.xlsx"
    data = load_data(file_path)

    if data is not None:
        # Filter options
        filter_options = st.sidebar.multiselect("Filter by:", ["Author", "Purchased", "Genre", "Status", "Series"])

        # Filter by author, purchased, genre, status, and series...
        # (Your existing filter code remains unchanged)

        # Display the filtered data
        st.table(data)  # Adjust the display as per your requirement

    # Add Book
    with st.sidebar.expander("Add Book"):
        book_title = st.text_input("Title")
        author = st.text_input("Author")
        series = st.text_input("Series")
        volume = st.text_input("Volume")
        purchased = st.radio("Purchased", options=["Purchased", "Not Purchased", "Not Released"])
        genre = st.text_input("Genres (comma-separated)")
        themes = st.text_input("Themes (comma-separated)")
        status = st.radio("Status", options=["Not Started", "Did Not Finish", "In Progress", "Finished", ""])
        rating = st.slider("Rating", min_value=0, max_value=10, step=1)

        if st.button("Add"):
            if book_title.strip() == "" or author.strip() == "":
                st.error("Title and Author are required!")
            else:
                # Convert comma-separated strings to lists
                genres_list = [genre.strip() for genre in genre.split(",")]
                themes_list = [theme.strip() for theme in themes.split(",")]

                new_book = pd.DataFrame({
                    'Title': [book_title],
                    'Author': [author],
                    'Series': [series],
                    'Volume': [volume],
                    'Purchased': [purchased],
                    'Genres': [genres_list],
                    'Themes': [themes_list],
                    'Status': [status],
                    'Rating': [rating],
                })
                data = pd.concat([data, new_book], ignore_index=True)
                save_data(data, file_path)
                st.success("Book added successfully!")
                st.experimental_rerun()

    # Create an expander for the "Edit Book" section
    with st.sidebar.expander("Edit Book"):
        # Initialize book_to_edit with an empty string
        book_to_edit = st.selectbox("Select Book to Edit", [""] + list(data['Title']))

        # Check if a book is selected
        if book_to_edit:
            selected_book = data[data['Title'] == book_to_edit].iloc[0]
            # Populate input fields with existing data
            new_title = st.text_input("New Title", selected_book['Title'])
            new_author = st.text_input("New Author", selected_book['Author'])
            new_series = st.text_input("New Series", selected_book['Series'])
            if new_series:
                new_volume = st.text_input("New Volume", selected_book['Volume'])
            new_purchased = st.radio("New Purchased", options=["Purchased", "Not Purchased", "Not Released"], index=int(selected_book['Purchased'] == "Purchased"))
            new_genre = st.text_input("New Genre", selected_book['Genre'])
            new_themes = st.text_input("New Themes", selected_book['Themes'])
            new_status = st.radio("New Status", options=["Not Started", "Did Not Finish", "In Progress", "Finished"], index=["Not Started", "Did Not Finish", "In Progress", "Finished", ""].index(selected_book['Status']))
            new_rating = st.slider("New Rating", min_value=0, max_value=10, step=1)
        if st.button("Update"):
            if new_title.strip() == "" or new_author.strip() == "":
                st.error("Title and Author are required!")
            else:
                data.loc[data['Title'] == book_to_edit, 'Title'] = new_title
                data.loc[data['Title'] == book_to_edit, 'Author'] = new_author
                data.loc[data['Title'] == book_to_edit, 'Series'] = new_series
                data.loc[data['Title'] == book_to_edit, 'Volume'] = new_volume
                data.loc[data['Title'] == book_to_edit, 'Purchased'] = new_purchased
                data.loc[data['Title'] == book_to_edit, 'Genre'] = new_genre
                data.loc[data['Title'] == book_to_edit, 'Themes'] = new_themes
                data.loc[data['Title'] == book_to_edit, 'Status'] = new_status
                data.loc[data['Title'] == book_to_edit, 'Rating'] = new_rating
                save_data(data, file_path)
                st.success("Book updated successfully!")
                st.experimental_rerun()


        # Allow user to remove a book
    with st.sidebar.expander("Remove Book"):
        book_to_remove = st.selectbox("Select Book to Remove", [""] + list(data['Title']))
        if st.button("Remove"):
            data = data[data['Title'] != book_to_remove]
            save_data(data, file_path)
            st.success("Book removed successfully!")
            st.experimental_rerun()

if __name__ == "__main__":
    main()
