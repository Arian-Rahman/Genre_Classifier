from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import csv


driver = webdriver.Firefox()

def get_subgenras(url):
    """
    Gets all the subgenra links and stores in genres.txt
    """
    try:
        #url = 'https://www.lyrics.com/style/Aboriginal'
        driver.get(url)
        wait = WebDriverWait(driver, 15)
        content_aside = wait.until(EC.presence_of_element_located((By.ID, 'content-aside')))
        # Step 3: Wait for the dropdown container within content-aside to load
        dropdown_container = WebDriverWait(content_aside, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.chosen-container.chosen-container-single'))
        )
        # Step 4: Trigger JavaScript events to open the dropdown within content-aside
        driver.execute_script("arguments[0].dispatchEvent(new Event('mouseover'))", dropdown_container)
        driver.execute_script("arguments[0].dispatchEvent(new Event('mousedown'))", dropdown_container)
        driver.execute_script("arguments[0].dispatchEvent(new Event('focus'))", dropdown_container)
        # Wait for the dropdown options to appear
        time.sleep(1)  # Allow some time for the options to load
        # Step 5: Trigger the mousewheel event to ensure the list is fully populated within content-aside
        driver.execute_script("arguments[0].dispatchEvent(new WheelEvent('mousewheel'))", dropdown_container)
        # Step 6: Extract the list items under the dropdown within content-aside
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.chosen-results li')))
        list_items = driver.find_elements(By.CSS_SELECTOR, 'ul.chosen-results li')
        # Step 7: Print the text content of each list item
        for item in list_items:
            print(item.text.strip())
        file_path = 'genres.txt'  # Define the file path
        # Open the file in write mode
        with open(file_path, 'w') as file:
            for item in list_items:
                # If item is a web element (like from BeautifulSoup), use .text
                if hasattr(item, 'text'):
                    item = item.text.strip()
                else:
                    item = item.strip()  # In case it's a string

                # Split the string by spaces, replace spaces with '+', and join the parts
                item = '+'.join(item.split())  # This replaces all spaces with '+'

                # Write each item on a new line
                item = f"https://www.lyrics.com/style/{item}"
                file.write(item + '\n')

        print(f"Saved output to {file_path}")
    finally:
        driver.quit()

def browse_specific_generas(base_url,genre_list,output_filename):
    '''
    Collects URLs for albums of genres listed in genres.txt and extracts album links across multiple pages.
    Saves the collected links to a file.
    '''
    driver = webdriver.Firefox()
    output_file = output_filename
    
    try:
        # Open the output file in append mode
        with open(output_file, "a") as file:
            # Read genre links from the genres.txt file
            with open(f"{genre_list}", "r") as f:
                genre_links = f.readlines()

            # Visit each base URL using Selenium
            for genre_link in genre_links:
                genre_link = genre_link.strip()  # Remove any extra whitespace
                genre_name = genre_link.split("/")[-1]  # Extract genre name from the URL
                print(f"Processing genre: {genre_name}")
                
                # Loop through pages 1 to 15 for each genre
                for page_number in range(1, 15):
                    paginated_url = f"{genre_link}/{page_number}"
                    print(f"Visiting URL: {paginated_url}")
                    
                    try:
                        driver.get(paginated_url)
                       # time.sleep(2)  # Wait for the page to load

                        # Find all sections with the specified class on the page
                        lyric_sections = driver.find_elements(By.CLASS_NAME, "sec-lyric")
                        
                        # Check if there are any sections on the current page
                        if not lyric_sections:
                            print(f"No more content on page {page_number}. Moving to the next genre.")
                            break

                        # Extract album links from each section
                        for section in lyric_sections:
                            try:
                                album_thumbs = section.find_elements(By.CLASS_NAME, "album-thumb")
                                
                                # Extract the href attribute from each anchor tag within album-thumb
                                for thumb in album_thumbs:
                                    try:
                                        link_element = thumb.find_element(By.TAG_NAME, "a")
                                        album_link = link_element.get_attribute("href")
                                        
                                        if album_link:
                                            print(f"Found album link: {album_link}")
                                            # Save the link to the file
                                            file.write(f"{genre_name},{album_link}\n")
                                    except NoSuchElementException:
                                        print("No hyperlink found in album-thumb.")
                            except NoSuchElementException:
                                print("No album-thumb divs found within section.")

                    except NoSuchElementException:
                        print(f"Page {page_number} does not exist for {genre_link}. Moving to the next genre.")
                        break
                    except Exception as e:
                        print(f"Unexpected error while processing {paginated_url}: {e}")
    
    finally:
        # Ensure the browser closes properly after processing
        driver.quit()


def browse_generas(base_url):
    '''
    Collects URLs for albums of genres listed in genres.txt and extracts album links across multiple pages.
    Saves the collected links to a file.
    '''
    driver = webdriver.Firefox()
    output_file = "links.txt"
    
    try:
        # Open the output file in append mode
        with open(output_file, "a") as file:
            # Read genre links from the genres.txt file
            with open("genres.txt", "r") as f:
                genre_links = f.readlines()

            # Visit each base URL using Selenium
            for genre_link in genre_links:
                genre_link = genre_link.strip()  # Remove any extra whitespace
                print(f"Processing genre: {genre_link}")
                
                # Loop through pages 1 to 15 for each genre
                for page_number in range(1, 16):
                    paginated_url = f"{genre_link}/{page_number}"
                    print(f"Visiting URL: {paginated_url}")
                    
                    try:
                        driver.get(paginated_url)
                       # time.sleep(2)  # Wait for the page to load

                        # Find all sections with the specified class on the page
                        lyric_sections = driver.find_elements(By.CLASS_NAME, "sec-lyric")
                        
                        # Check if there are any sections on the current page
                        if not lyric_sections:
                            print(f"No more content on page {page_number}. Moving to the next genre.")
                            break

                        # Extract album links from each section
                        for section in lyric_sections:
                            try:
                                album_thumbs = section.find_elements(By.CLASS_NAME, "album-thumb")
                                
                                # Extract the href attribute from each anchor tag within album-thumb
                                for thumb in album_thumbs:
                                    try:
                                        link_element = thumb.find_element(By.TAG_NAME, "a")
                                        album_link = link_element.get_attribute("href")
                                        
                                        if album_link:
                                            print(f"Found album link: {album_link}")
                                            # Save the link to the file
                                            file.write(f"{album_link}\n")
                                    except NoSuchElementException:
                                        print("No hyperlink found in album-thumb.")
                            except NoSuchElementException:
                                print("No album-thumb divs found within section.")

                    except NoSuchElementException:
                        print(f"Page {page_number} does not exist for {genre_link}. Moving to the next genre.")
                        break
                    except Exception as e:
                        print(f"Unexpected error while processing {paginated_url}: {e}")
    
    finally:
        # Ensure the browser closes properly after processing
        driver.quit()

def extract_song_links_from_album(input_file, output_file, placeholder_genre):
    '''
    Reads album URLs from a file, scrapes song links from each album URL, 
    and saves them to a new file along with two comma-separated genres.
    '''
    driver = webdriver.Firefox()

    try:
        # Read lines from the input file
        with open(input_file, "r") as file:
            lines = file.readlines()

        # Open the output file in append mode
        with open(output_file, "a") as output:
            for line in lines:
                line = line.strip()  # Remove any extra spaces/newlines
                if not line:
                    continue

                # Split the line into genre and URL
                try:
                    genre, album_url = line.split(",", 1)
                except ValueError:
                    print(f"Skipping malformed line: {line}")
                    continue

                print(f"Processing Album: {album_url} for Genre: {genre}")

                try:
                    driver.get(album_url)

                    # Scrape all relevant song links on the page
                    # Locate all 'a' tags inside <strong> elements within the specified table structure
                    song_links = driver.find_elements(By.CSS_SELECTOR, "tbody tr td strong a")

                    for link in song_links:
                        song_url = link.get_attribute("href")
                        if song_url:
                            print(f"Found song link: {song_url}")
                            # Write the genres and song link to the output file
                            output.write(f"{placeholder_genre},{genre},{song_url}\n")

                except NoSuchElementException:
                    print(f"No elements found on {album_url}. Skipping.")
                except Exception as e:
                    print(f"Error while processing {album_url}: {e}")

    finally:
        driver.quit()


def scrape_additional_links(input_file, output_file):
    '''
    Reads URLs from a file, scrapes additional links from each URL, and saves them to a new file.
    '''
    driver = webdriver.Firefox()

    try:
        # Read links from the input file
        with open(input_file, "r") as file:
            urls = file.readlines()

        # Open the output file in append mode
        with open(output_file, "a") as output:
            for url in urls:
                url = url.strip()  # Remove any extra spaces/newlines
                if not url:
                    continue

                print(f"Visiting URL: {url}")
                try:
                    driver.get(url)

                    # Scrape all relevant links on the page based on the HTML structure you provided
                    # Locate all 'a' tags inside the <strong> elements within the specified table structure
                    links = driver.find_elements(By.CSS_SELECTOR, "tbody tr td strong a")

                    for link in links:
                        href = link.get_attribute("href")
                        if href:
                            print(f"Found link: {href}")
                            output.write(f"{href}\n")

                except NoSuchElementException:
                    print(f"No elements found on {url}. Skipping.")
                except Exception as e:
                    print(f"Error while processing {url}: {e}")

    finally:
        driver.quit()



def extract_song_and_details_with_custom_genre(input_file, output_file):
    '''
    Extracts song titles, artist names, lyrics, and genre/subgenre from links and saves them to a CSV. Adds main genere as well
    '''
    driver = webdriver.Firefox()  # Initialize the WebDriver
    try:
        with open(output_file, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Song Title', 'Artist', 'Lyrics', 'Genres'])  # Adjusted CSV header
            # Read URLs from the input file
            with open(input_file, "r") as file:
                urls = file.readlines()

            for url in urls:
                url = url.strip()
                main_genre,subgenre,url = url.split(",", 2)
                subgenre = subgenre.replace("+", " ")
                if not url:
                    continue
                
                print(f"Processing: {url}")
                try:
                    driver.get(url)
                    time.sleep(1)  # Adjust sleep time for page load
                    # Extract song title
                    try:
                        song_title = driver.find_element(By.CSS_SELECTOR, "h1.lyric-title").text
                    except NoSuchElementException:
                        song_title = "Unknown Title"
                    # Extract artist name
                    try:
                        artist_name = driver.find_element(By.CSS_SELECTOR, "h3.lyric-artist a").text
                    except NoSuchElementException:
                        artist_name = "Unknown Artist"
                    # Extract lyrics
                    try:
                        lyrics_element = driver.find_element(By.CSS_SELECTOR, "pre#lyric-body-text")
                        lyrics = lyrics_element.text.replace("\n", " ** ")
                    except NoSuchElementException:
                        lyrics = "No Lyrics Found"

                    # Extract genres (from the first column)
                    genres = []
                    try:
                        genre_elements = driver.find_elements(By.CSS_SELECTOR, "div.col-sm-6:first-child a.small")
                        for genre_element in genre_elements:
                            genres.append(genre_element.text)
                    except NoSuchElementException:
                        genres = []
                    # Extract subgenres (from the second column)
                    subgenres = []
                    try:
                        subgenre_elements = driver.find_elements(By.CSS_SELECTOR, "div.col-sm-6:nth-child(2) a.small")
                        for subgenre_element in subgenre_elements:
                            subgenres.append(subgenre_element.text)
                    except NoSuchElementException:
                        subgenres = []

                    # Combine custom genres,genres and subgenres
                    main_genres = [main_genre,subgenre]
                    genres_text = ", ".join(main_genres+genres + subgenres)
                    # Skip saving the song if both genres and subgenres are empty
                    if not genres_text.strip():
                        print(f"Skipping: {song_title} by {artist_name} (No genre found)")
                        continue
                    with open("logger.txt", "w") as output:
                            output.write(f" Last Genre :{main_genre} , {subgenre} \n Latest Song Accessed :{url}\n")

                    # Write the extracted data to the CSV
                    writer.writerow([song_title, artist_name, lyrics, genres_text])
                    print(f"Saved: {song_title} by {artist_name} with Genres: {genres_text}")
                except Exception as e:
                    print(f"Error processing {url}: {e}")
    finally:
        driver.quit()

# def extract_song_and_details(input_file, output_file):
#     '''
#     Extracts song titles, artist names, lyrics, and genre/subgenre from links and saves them to a CSV.
#     '''
#     driver = webdriver.Firefox()  # Initialize the WebDriver
#     try:
#         with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerow(['Song Title', 'Artist', 'Lyrics', 'Genres'])  # Adjusted CSV header
            
#             # Read URLs from the input file
#             with open(input_file, "r") as file:
#                 urls = file.readlines()

#             for url in urls:
#                 url = url.strip()
#                 if not url:
#                     continue
                
#                 print(f"Processing: {url}")
#                 try:
#                     driver.get(url)
#                     time.sleep(1)  # Adjust sleep time for page load

#                     # Extract song title
#                     try:
#                         song_title = driver.find_element(By.CSS_SELECTOR, "h1.lyric-title").text
#                     except NoSuchElementException:
#                         song_title = "Unknown Title"

#                     # Extract artist name
#                     try:
#                         artist_name = driver.find_element(By.CSS_SELECTOR, "h3.lyric-artist a").text
#                     except NoSuchElementException:
#                         artist_name = "Unknown Artist"

#                     # Extract lyrics
#                     try:
#                         lyrics_element = driver.find_element(By.CSS_SELECTOR, "pre#lyric-body-text")
#                         lyrics = lyrics_element.text.replace("\n", " ** ")
#                     except NoSuchElementException:
#                         lyrics = "No Lyrics Found"

#                     # Extract genres (from the first column)
#                     genres = []
#                     try:
#                         genre_elements = driver.find_elements(By.CSS_SELECTOR, "div.col-sm-6:first-child a.small")
#                         for genre_element in genre_elements:
#                             genres.append(genre_element.text)
#                     except NoSuchElementException:
#                         genres = []

#                     # Extract subgenres (from the second column)
#                     subgenres = []
#                     try:
#                         subgenre_elements = driver.find_elements(By.CSS_SELECTOR, "div.col-sm-6:nth-child(2) a.small")
#                         for subgenre_element in subgenre_elements:
#                             subgenres.append(subgenre_element.text)
#                     except NoSuchElementException:
#                         subgenres = []

#                     # Combine genres and subgenres
#                     genres_text = ", ".join(genres + subgenres)

#                     # Skip saving the song if both genres and subgenres are empty
#                     if not genres_text.strip():
#                         print(f"Skipping: {song_title} by {artist_name} (No genre found)")
#                         continue

#                     # Write the extracted data to the CSV
#                     writer.writerow([song_title, artist_name, lyrics, genres_text])
#                     print(f"Saved: {song_title} by {artist_name} with Genres: {genres_text}")

#                 except Exception as e:
#                     print(f"Error processing {url}: {e}")

#     finally:
#         driver.quit()


def main():
    base_url = "https://www.lyrics.com/style/"
    # url = "https://www.lyrics.com/style/Aboriginal"
    # # run it once, filter from the file 
    # #get_subgenras(url)
    # browse_generas(base_url)
    # scrape_additional_links(input_file="links.txt",output_file="album_songs.txt")

    # Example usage:
    #input_file = "album_songs.txt"  # Links file
    #output_file = "song_artist.csv"   # Output CSV file
    #extract_song_and_details(input_file, output_file)


    #Scraping for imbalanced data 
    #browse_specific_generas(base_url,'genres_rock.txt','links_rock.txt')
    #extract_song_links_from_album(input_file="links_rock.txt", output_file="rock_album_songs.txt", placeholder_genre="Rock")
    #browse_specific_generas(base_url,'genre_files/genres_metal.txt','album_list_by_genre/links_metal.txt')
    #extract_song_links_from_album(input_file="album_list_by_genre/links_metal.txt", output_file="song_list_files/metal_album_songs.txt", placeholder_genre="Rock")
    #browse_specific_generas(base_url,'genre_files/genres_blues.txt','album_list_by_genre/links_blues.txt')
    #extract_song_links_from_album(input_file="album_list_by_genre/links_blues.txt", output_file="song_list_files/blues_album_songs.txt", placeholder_genre="Rock")
    # browse_specific_generas(base_url,'genre_files/genres_pop.txt','album_list_by_genre/links_pop.txt')
    # extract_song_links_from_album(input_file="album_list_by_genre/links_pop.txt", output_file="song_list_files/pop_album_songs.txt", placeholder_genre="Rock")
    #browse_specific_generas(base_url,'genre_files/genres_country.txt','album_list_by_genre/links_country.txt')
    #extract_song_links_from_album(input_file="album_list_by_genre/links_country.txt", output_file="song_list_files/country_album_songs.txt", placeholder_genre="country")
    genres = ["rock","blues","country","metal","pop","other"]
    for genre in genres:
        print(f"Processing Genre  : {genre}")
        extract_song_and_details_with_custom_genre(input_file=f"song_list_files/{genre}_album_songs.txt", output_file="songs_data.csv")

    


if __name__ == "__main__":
    main()
