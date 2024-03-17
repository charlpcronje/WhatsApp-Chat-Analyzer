# app.py
import json
import os
import re
from datetime import datetime, timedelta
from collections import defaultdict

class WhatsAppChatAnalyzer:
    """
    This class processes a WhatsApp chat export file to separate messages between two specified individuals,
    excluding messages that contain specified phrases. It calculates and outputs statistics such as the total
    word count, top 10 active days, and average response time for each individual. The results are saved in
    Markdown files.
    """
    
    def __init__(self, config_path):
        """
        Initializes the WhatsAppChatAnalyzer with the path to a configuration JSON file.
        Loads the configuration upon initialization.
        """
        self.config = self.load_config(config_path)
        print("Configuration loaded successfully.")
    
    def load_config(self, config_path):
        """Loads configuration from a JSON file specified by config_path."""
        with open(config_path, 'r') as file:
            return json.load(file)
    
    def clean_message(self, message):
        """Cleans the message by removing phrases to ignore."""
        for phrase in self.config['phrases_to_ignore']:
            message = message.replace(phrase, '').strip()
        return message
    
    # M-app-process_chat-A-3
    def process_chat(self):
        print("Processing chat file...")
        file_path = self.config['whatsapp_export_path']
        person1, person2 = self.config['person1'], self.config['person2']
        messages = defaultdict(list)
        person1_dates_words = defaultdict(int)
        person2_dates_words = defaultdict(int)
        person1_word_count = 0
        person2_word_count = 0
        response_times = {person1: [], person2: []}
        prev_timestamp = None
        prev_author = None

        with open(file_path, 'r', encoding='utf-8') as f:
            message_buffer = ""
            for line in f:
                match = re.match(r'^(\d{4}/\d{2}/\d{2}), (\d{2}:\d{2}) - (.*?): (.*)', line)
                if match:
                    if message_buffer:
                        if prev_author == person1:
                            person1_word_count = self.process_message(message_buffer, messages, person1_dates_words, person1_word_count, response_times, prev_timestamp, prev_author)
                        elif prev_author == person2:
                            person2_word_count = self.process_message(message_buffer, messages, person2_dates_words, person2_word_count, response_times, prev_timestamp, prev_author)
                    date_str, time_str, author, text = match.groups()
                    message_buffer = text.strip()
                    if author in [person1, person2]:
                        prev_timestamp = datetime.strptime(f"{date_str} {time_str}", "%Y/%m/%d %H:%M")
                        prev_author = author
                else:
                    message_buffer += " " + line.strip()

            if message_buffer:
                if prev_author == person1:
                    person1_word_count = self.process_message(message_buffer, messages, person1_dates_words, person1_word_count, response_times, prev_timestamp, prev_author)
                elif prev_author == person2:
                    person2_word_count = self.process_message(message_buffer, messages, person2_dates_words, person2_word_count, response_times, prev_timestamp, prev_author)

        person1_top_days = sorted(person1_dates_words.items(), key=lambda x: x[1], reverse=True)[:10]
        person2_top_days = sorted(person2_dates_words.items(), key=lambda x: x[1], reverse=True)[:10]

        avg_response_times = {}
        avg_response_times_trimmed = {}
        for person in [person1, person2]:
            if response_times[person]:
                avg_response_times[person] = self.calculate_average_response_time([rt[1] for rt in response_times[person]], trim_outliers=False)
                avg_response_times_trimmed[person] = self.calculate_average_response_time([rt[1] for rt in response_times[person]], trim_outliers=True)
            else:
                avg_response_times[person] = timedelta(seconds=0)
                avg_response_times_trimmed[person] = timedelta(seconds=0)

        print("Chat file processed successfully.")
        return messages, person1_word_count, person2_word_count, person1_top_days, person2_top_days, avg_response_times, avg_response_times_trimmed

    # M-app-process_message-A-1
    def process_message(self, message, messages, dates_words, total_word_count, response_times, prev_timestamp, prev_author):
        cleaned_message = self.clean_message(message)
        if cleaned_message:
            word_count = len(cleaned_message.split())
            total_word_count += word_count
            if prev_timestamp:
                date_str = prev_timestamp.strftime("%Y/%m/%d")
                dates_words[date_str] += word_count
                if prev_author in [self.config['person1'], self.config['person2']]:
                    messages[prev_author].append((prev_timestamp.strftime("%Y/%m/%d %H:%M"), cleaned_message))
                    if response_times[prev_author]:
                        response_times[prev_author].append((prev_timestamp, (prev_timestamp - response_times[prev_author][-1][0]).total_seconds()))
                    else:
                        response_times[prev_author].append((prev_timestamp, 0))
        return total_word_count

    # M-app-calculate_average_response_time-A-1
    def calculate_average_response_time(self, response_times, trim_outliers=True):
        if not response_times:
            return timedelta(seconds=0)
        if trim_outliers:
            response_times = sorted(response_times)
            n = len(response_times)
            if n <= 2:
                return timedelta(seconds=sum(response_times) / n)
            else:
                # Exclude outliers (top and bottom 10% of response times)
                k = int(n * 0.1)
                trimmed_response_times = response_times[k:n-k]
                return timedelta(seconds=sum(trimmed_response_times) / len(trimmed_response_times))
        else:
            return timedelta(seconds=sum(response_times) / len(response_times))
    
    # M-app-write_to_file-A-3
    def write_to_file(self, messages, person1_word_count, person2_word_count, person1_top_days, person2_top_days, avg_response_times, avg_response_times_trimmed):
        print("Writing messages to files...")
        base_path = f"./messages/{self.config['person1']}_{self.config['person2']}"

        if not os.path.exists(base_path):
            os.makedirs(base_path)

        for person, word_count, top_days, avg_response_time, avg_response_time_trimmed in zip(
            [self.config['person1'], self.config['person2']],
            [person1_word_count, person2_word_count],
            [person1_top_days, person2_top_days],
            [avg_response_times[self.config['person1']], avg_response_times[self.config['person2']]],
            [avg_response_times_trimmed[self.config['person1']], avg_response_times_trimmed[self.config['person2']]]
        ):
            file_path = os.path.join(base_path, f'{person}.md')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {person}\n\n")
                f.write(f"Total words: {word_count}\n\n")
                f.write("## Top 10 Days by Word Count\n")
                for date, count in top_days:
                    f.write(f"- **{date}**: {count} words\n")
                f.write(f"\n## Average Response Time\n")
                f.write(f"- **{person}**: {avg_response_time}\n")
                f.write(f"- **{person}** (trimmed outliers): {avg_response_time_trimmed}\n")
                f.write("\n## Messages\n")
                for datetime_str, msg in messages[person]:
                    if msg.strip():
                        f.write(f"- **{datetime_str}**: {msg}\n")

        print("Messages written to files successfully.")


# M-app-main-B-3
def main():
    config_path = 'config.json'
    analyzer = WhatsAppChatAnalyzer(config_path)
    messages, person1_word_count, person2_word_count, person1_top_days, person2_top_days, avg_response_times, avg_response_times_trimmed = analyzer.process_chat()
    analyzer.write_to_file(messages, person1_word_count, person2_word_count, person1_top_days, person2_top_days, avg_response_times, avg_response_times_trimmed)
    print("Analysis complete. Check the output files for details.")

if __name__ == "__main__":
    main()