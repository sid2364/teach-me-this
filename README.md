# teach-me-this

Use a Retrieval Augmented Generation (RAG) system alongside an open source LLM from HuggingFace to allow you to ask questions based on specific information in a PDF. Nothing fancy, using 3rd party libs: HuggingFace, LanceDB, Langchain

### Future work

Idea is to extend this functionality to be used for any document that can be tokenized and "searched" through once put into a vector database. For the POC, I used the LOTR books and asked deep-cut questions, and it mostly(?) worked!

Could (in theory) be used by students to use an LLM to ask questions about subject material. Or just to be able to brainstorm with a document as context.

Web UI can be added as a front to upload any document. Creating an instance of LanceDB with all the chunks from the doc is the main bottle-neck - for my local system, it took about 4-5 minutes everytime just for this operation. Once the backend has been modularised and some API endpoints have been written to do these operations, the UI should be trivial.

## How to run

#### Upgrade pip in the virtual environment

```
pip install --upgrade pip
```

#### Install required dependencies

```
pip3 install -r requirements.txt
```

#### Place PDFs in `/data` folder

#### Run `main.py`

```
python main.py
```

## Sample output

This is when data/ is added with the Silmarillion by JRR Tolkien

```text
You are a helpful AI assistant. Your name is Jarvis

Use the following information fetched from the PDF provided by the user to answer the question:
of their voyage, and were taken from them for ever. Then Eärendil said to Elwing: 'Await me here; for one only may bring the message that it is my fate to bear.' And he went up alone into the land, and came into the Calacirya, and it seemed to him empty and silent; for even as Morgoth and Ungoliant came in ages past, so now Eärendil had come at a time of festival, and wellnigh all the Elvenfolk were gone to Valimar, or were gathered in the halls of
of the ships of song; golden were its oars and white its timbers, hewn in the birchwoods of Nimbrethil, and its sails were as the argent moon. In the Lay of Eärendil is many a thing sung of his adventures in the deep and in lands untrodden, and in many seas and in many isles; but Elwing was not with him, and she sat in sorrow by the mouths of Sirion. Eärendil found not Tuor nor Idril, nor came he ever on that journey to the shores of Valinor, defeated by shadows and enchantment, driven by repelling winds, until in longing for Elwing he turned homeward towards the coast of Beleriand. And his heart bade him haste, for a sudden fear had fallen on him out of dreams; and the winds that before he had striven with might not now bear him back as swift as his desire. Now when first the tidings came to Maedhros that Elwing yet lived, and dwelt in possession of the Silmaril by the mouths of Sirion, he repenting of the deeds in Doriath withheld his hand. But in time the knowledge of their oath
the Teleri saw the coming of that ship out of the East and they were amazed, gazing from afar upon the light of the Silmaril, and it was very great. Then Eärendil, first of living Men, landed on the immortal shores; and he spoke there to Elwing and to those that were with him, and they were three mariners who had sailed all the seas besides him: Falathar, Erellont, and Aerandir were their names. And Eärendil said to them: 'Here none but myself shall set foot, lest you fall under the wrath of the Valar. But that peril I will take on myself alone, for the sake of the Two Kindreds.' But Elwing answered: 'Then would our paths be sundered for ever; but all thy perils I will take on myself also.' And she leaped into the white foam and ran towards him; but Eärendil was sorrowful, for he feared the anger of the Lords of the West upon any of Middle-earth that should dare to pass the leaguer of Aman. And there they bade farewell to the companions of their voyage, and were taken from them for

Question: What did Eärendil say to Elwing before he went up alone into the land and came into the Calacirya?
Answer:

Eärendil said to Elwing: 'Await me here; for one only may bring the message that it is my fate to bear.' (Source: The PDF provided by the user)
```

... which is correct!
