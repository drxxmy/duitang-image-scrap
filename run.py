from main import DuitangParser

if __name__ == "__main__":
    keyword = input("Enter a keyword to search for images: ")
    scroll_number = int(input("Enter the page load depth in scroll numbers: "))
    sleep_timer = int(input("Enter the sleep timer after scrolling: "))
    dp = DuitangParser(
        keyword=keyword, scroll_number=scroll_number, sleep_timer=sleep_timer
    )
    dp.run()
