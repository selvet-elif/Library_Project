import asyncio

from library import Library
from openlibrary import fetch_book_from_api


def main():
    library = Library(name="City Library")

    while True:
        print("\n--- Kitap Yönetim Sistemi ---")
        print("1. Kitap Ekle")
        print("2. Kitap Sil")
        print("3. Kitapları Listele")
        print("4. Kitap Ara")
        print("5. Çıkış")

        choice = input("Seçiminizi yapın: ")

        if choice == "1":
            isbn = input("ISBN: ")
            try:
                book = asyncio.run(fetch_book_from_api(isbn))
                library.add_book(book)
            except Exception as exc:
                print(f"Kitap eklenemedi: {exc}")
        elif choice == "2":
            isbn = input("Silmek istediğiniz kitabın ISBN'i: ")
            if not library.delete_book(isbn):
                print("Kitap bulunamadı.")
        elif choice == "3":
            print("Kitap listesi:")
            for info in library.list_books():
                print("-", info)
        elif choice == "4":
            title = input("Aranacak kitabın adı: ")
            result = library.find_book(title=title)
            if result:
                print(result.display_info())
            else:
                print("Kitap bulunamadı.")
        elif choice == "5":
            print("Programdan çıkılıyor...")
            break
        else:
            print("Geçersiz seçim, tekrar deneyin.")


if __name__ == "__main__":
    main()
