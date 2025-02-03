import tkinter as tk
from tkinter import scrolledtext, messagebox, Toplevel
import feedparser
import webbrowser

class NewsParserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Парсер новостей")
        self.root.geometry("600x400")
        self.root.configure(bg='#2E2E2E')  # Темно-серый фон

        self.url_label = tk.Label(root, text="Введите URL RSS-ленты:", bg='#2E2E2E', fg='white',
                                  font=("Times New Roman", 12))
        self.url_label.pack(pady=10)

        self.url_entry = tk.Entry(root, width=50, font=("Times New Roman", 12))
        self.url_entry.pack(pady=5)

        self.paste_button = tk.Button(root, text="Вставить", command=self.paste_url, bg='green', fg='white',
                                      font=("Times New Roman", 12))
        self.paste_button.pack(pady=5)

        self.parse_button = tk.Button(root, text="Парсить", command=self.parse_rss, bg='red', fg='white',
                                      font=("Times New Roman", 12))
        self.parse_button.pack(pady=10)

        self.list_button = tk.Button(root, text="Список RSS лент", command=self.open_rss_list, bg='yellow', fg='black',
                                     font=("Times New Roman", 12))
        self.list_button.pack(pady=5)

        # Поле для вывода результатов парсинга
        self.output_text = scrolledtext.ScrolledText(root, bg='white', fg='black', insertbackground='black',
                                                     font=("Times New Roman", 12))
        self.output_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Настройка стилей для заголовков и ссылок
        self.output_text.tag_configure("title", font=("Times New Roman", 12, "bold"),
                                       foreground="black")  # Заголовок с увеличенным шрифтом
        self.output_text.tag_configure("link", foreground="blue", underline=True)  # Ссылка синим и подчеркиванием
        self.output_text.bind("<Button-1>", self.open_link)  # Привязка клика мыши к функции
        self.output_text.bind("<Motion>", self.change_cursor)  # Привязка движения мыши к функции

    def paste_url(self):
        try:
            clipboard_content = self.root.clipboard_get()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, clipboard_content)
        except tk.TclError:
            messagebox.showwarning("Предупреждение", "Буфер обмена пуст.")

    def parse_rss(self):
        rss_url = self.url_entry.get().strip()
        if not rss_url:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите URL.")
            return

        feed = feedparser.parse(rss_url)

        if feed.bozo == 0:
            self.output_text.delete(1.0, tk.END)  # Очистка текста
            for entry in feed.entries:
                title = entry.title
                link = entry.link
                self.output_text.insert(tk.END, f"{title}\n", "title")  # Выводим только заголовок

                link_start = self.output_text.index(tk.END) # Получение индекса начала ссылки
                self.output_text.insert(tk.END, f"{link}\n", "link")  # Выводим ссылку
                link_end = self.output_text.index(tk.END) # Получение индекса конца ссылки
                self.output_text.tag_add("link", link_start, link_end) # Добавление тега "link" на строку
                self.output_text.insert(tk.END, "\n") # пустая строка, что бы отделить ссылки

        else:
            messagebox.showerror("Ошибка", "Не удалось парсить RSS-ленту. Проверьте правильность URL.")

    def open_link(self, event):
        for tag in self.output_text.tag_names(tk.CURRENT):
            if tag == "link":
                index = self.output_text.index("@%s,%s" % (event.x, event.y))
                start = self.output_text.index(f"{index} linestart")
                end = self.output_text.index(f"{index} lineend")
                link = self.output_text.get(start, end).strip()
                webbrowser.open(link)
                return

    def change_cursor(self, event):
        for tag in self.output_text.tag_names(tk.CURRENT):
            if tag == "link":
                self.output_text.config(cursor="hand2")
                return
        self.output_text.config(cursor="")

    def open_rss_list(self):
        rss_list_window = Toplevel(self.root)
        rss_list_window.title("Список RSS лент")
        rss_list_window.geometry("400x300")
        rss_list_window.configure(bg='#2E2E2E')

        categories = {
            "Общие новости": [
                "https://lenta.ru/rss/",
                "https://ria.ru/export/rss2/index.xml",
                "https://tass.ru/rss/v2.xml",
                "https://www.interfax.ru/rss.asp",
                "https://www.kommersant.ru/RSS/main.xml"
            ],
            "Новости (отдельная категория)": [
                "https://lenta.ru/rss/news/",
                "https://www.kommersant.ru/RSS/news.xml"
            ],
            "Статьи": [
                "https://lenta.ru/rss/articles/",
                "https://habr.com/ru/rss/articles/"
            ],
            "Технологии": [
                "https://habr.com/ru/rss/all/",
                "https://habr.com/ru/rss/news/",
                "https://www.opennet.ru/opennews/opennews_all.rss"
            ]
        }

        for category, links in categories.items():
            category_label = tk.Label(rss_list_window, text=category, bg='#2E2E2E', fg='white',
                                      font=("Times New Roman", 12))
            category_label.pack(pady=5)

            for link in links:
                link_button = tk.Button(rss_list_window, text=link,
                                        command=lambda l=link: self.copy_to_entry_and_close(rss_list_window, l),
                                        bg='#3E3E3E', fg='white', anchor='w', width=50, font=("Times New Roman", 12))
                link_button.pack(pady=2)


    def copy_to_entry_and_close(self, rss_list_window, link):
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, link)
        rss_list_window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = NewsParserApp(root)
    root.mainloop()