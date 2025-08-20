from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests

# --- SETUP SELENIUM ---
options = Options()
options.add_argument("--disable-popup-blocking")
driver = webdriver.Chrome(options=options)

# --- STEP 1: Open the site ---
driver.get("https://studentportal.inokomis.in/Newstudent/WeLectures")  # 🔁 Replace with actual URL
driver.maximize_window()
time.sleep(95)

# --- STEP 2: Find all "View" buttons ---
view_buttons = driver.find_elements(By.XPATH, "//button[text()='View']")

print(f"Found {len(view_buttons)} videos.")

# --- STEP 3: Loop through each button ---
for index in range(len(view_buttons)):
    # Re-locate buttons every time to avoid stale element reference
    view_buttons = driver.find_elements(By.XPATH, "//button[text()='View']")
    
    try:
        # Click the View button
        view_buttons[index].click()
        time.sleep(3)

        # Wait for popup/tab to open and switch to it
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(3)

        # Try finding video element
        try:
            video = driver.find_element(By.TAG_NAME, "video")
            video_url = video.get_attribute("src")
        except:
            video_url = None

        if video_url:
            print(f"📥 Downloading video {index+1} from: {video_url}")
            r = requests.get(video_url)
            with open(f"video_{index+1}.mp4", "wb") as f:
                f.write(r.content)
            print(f"✅ Downloaded: video_{index+1}.mp4")
        else:
            print(f"❌ Video URL not found for item {index+1}.")

        # Close popup/tab and return to main page
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)

    except Exception as e:
        print(f"⚠️ Error at video {index+1}: {e}")
        driver.switch_to.window(driver.window_handles[0])

# --- STEP 4: Done ---
print("✅ All done.")
driver.quit()
