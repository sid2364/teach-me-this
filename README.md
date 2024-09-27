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

## An academic example
When passed a whitepaper about rent division with picky roommates (credit: https://arxiv.org/pdf/2409.14600 for the brilliant source material), and cross-examined, this is the output:
```commandline
env) sid@wolfpack:~/Study/teach-me-this$ python3 main.py 
USER_AGENT environment variable not set, consider setting it to identify your requests.
/home/sid/Study/teach-me-this/env/lib/python3.12/site-packages/transformers/tokenization_utils_base.py:1601: FutureWarning: `clean_up_tokenization_spaces` was not set. It will be set to `True` by default. This behavior will be depracted in transformers v4.45, and will be then set to `False` by default. For more details check this issue: https://github.com/huggingface/transformers/issues/31884
  warnings.warn(
Firing things up... This may take a minute (or three)
Reading books: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00,  2.74it/s]
Splitting documents: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 37/37 [00:00<00:00, 3903.25it/s]
Chunk 1:
0(e log d time), 1999. [5] Marek Cygan. Improved approximation for 3-dimensional matching via bounded pathwidth local search. In2013 IEEE 54th Annual Symposium on Foundations of Computer Science , pages 509–518, 2013. doi:10.1109/FOCS.2013.61. [6] Ya’akov Gal, Moshe Mash, Ariel D Procaccia, and Yair Zick. Which is the fairest (rent division) of them all? In Proceedings of the 2016 ACM Conference on Economics and Computation , pages 67–84, 2016. [7] Ashish Goel, Michael Kapralov, and Sanjeev Khanna. Perfect matchings in o(nlogn)time in regular bipartite graphs, 2010. [8] Martin Grotschel, Laszlo Lovasz, and Alexander Schrijver. Geometric algorithms and combinatorial optimiza- tion. Springer, 1993. [9] Harold W. Kuhn. The hungarian method for the assignment problem. Naval Research Logistics Quarterly , 1956. [10] Dominik Peters, Ariel D. Procaccia, and David Zhu. Robust rent division. In Alice H. Oh, Alekh Agarwal, Danielle Belgrave, and Kyunghyun Cho, editors, Advances in Neural

Chunk 2:
and Kyunghyun Cho, editors, Advances in Neural Information Processing Systems , 2022. URL https://openreview.net/forum?id=eRBVi61Vct1 . [11] Ariel Procaccia, Rodrigo Velez, and Dingli Yu. Fair rent division on a budget. Proceedings of the AAAI Conference on Artificial Intelligence , 32(1), 2018. ISSN 2374-3468. doi:10.1609/aaai.v32i1.11465. URL https://ojs.aaai.org/index.php/AAAI/article/view/11465 . Number: 1. [12] Ariel D. Procaccia, Benjamin Schiffer, and Shirley Zhang. Multi-apartment rent division, 2024. [13] Rodrigo A. Velez. Equitable rent division. ACM Trans. Econ. Comput. , 6(2), 2018. ISSN 2167-8375. doi:10.1145/3274528. URL https://dl.acm.org/doi/10.1145/3274528 . 14

384
The token has not been saved to the git credentials helper. Pass `add_to_git_credential=True` in this function directly or `--add-to-git-credential` if using via `huggingface-cli` if you want to set the git credential as well.
Token is valid (permission: read).
Your token has been saved to /home/sid/.cache/huggingface/token
Login successful



Ask me anything about the books you asked me to read: data/2409.16579v1.pdfdata/2409.14600v1.pdf!
(type 'exit' to end conversation)

You: What is the rent game about?

Jarvis: 
The rent game is a problem in computer science and economics that deals with dividing rent among tenants in a fair and efficient manner. In this context, fairness is defined as ensuring that every given participant prefers his or her assignment over that of everyone else, which is called envy-freeness. This paper explores how to account for room and roommate preferences when rent division is extended to include roommates, which is a consideration that requires new analysis. The authors present novel algorithmic approaches to find the maximum social welfare assignment and produce prices that minimize tenant envy to ensure fairness. The problem is not straightforward as previous research tools no longer apply directly to the setting with roommates. The authors provide a guarantee of roommate envy-freeness and present an integer program to minimize envy among tenants. The existence of a person envy-free price vector for the max-welfare assignment is not guaranteed, as shown in a counterexample.
--------------------

You: What happens when a person wants to pay more for a room? How do you ensure fairness?

Jarvis: In the context of the roommate rent division problem, if a person wants to pay more for a room, it is possible to ensure fairness by implementing a price vector that minimizes tenant envy. This can be achieved by using the ε-EF (ε-envy-freeness) fairness concept, which ensures that one's utility for rooming with someone else is at most ε times what they currently receive given the max welfare assignment. To achieve this, we present constructions with both equal and unequal splitting of rent among roommates, alongside the general option. The proposed algorithms and fairness guarantees are tested in numerical results, and the results show that the proposed approaches are promising solutions that balance fairness and efficiency.
--------------------

You: Is it a zero-sum game?

Jarvis: 
Hedonic games, including the ones introduced in this paper, are not necessarily zero-sum games. In hedonic games, agents have their own preferences over coalitions, and their utility is determined by the coalition they belong to, not necessarily by the coalition they are not a part of. Therefore, the utility of one agent does not necessarily correspond to the loss of another agent.
--------------------

```
Still need to keep up with the changes in the HuggingFace libraries to remove wanrings, but so far so good!


## A less academic example
This is when data/ is added with the Silmarillion by JRR Tolkien
```text
You: What did Eärendil say to Elwing before he went up alone into the land and came into the Calacirya?
Jarvis: Eärendil said to Elwing: 'Await me here; for one only may bring the message that it is my fate to bear.' (Source: The PDF provided by the user)
```
... which is correct!