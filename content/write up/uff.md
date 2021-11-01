---
title: Blitzeinführung in NLP
slug: uff
date: 2021-10-30 21:55:02 +0100
lang: de
publications_src: content/til.bib
--- 

Moin! Herzlich Willkommen zu den Ressoursen für meinen Talk *NLP - eine Interaktive Blitzeinführung* auf dem [University Future Festival 2021](https://festival.hfd.digital/en/open-for-discussion/conference-day/). Hier findet sich sowohl Links zu den Quellen meines Talks, Weiterführendes um sich intensiver zu beschäftigen als auch der Programmcode zum direkt kopieren und ausführen.
Aber am Besten klickt man auf einen der Beiden Links um direkt in einer interaktiven Umgebung arbeiten zu können: 

<a href='https://colab.research.google.com/github/hno2/uff/blob/main/Beispiele.ipynb' target="_blank"><img src='/images/icons/colab-badge.svg' style="width:10vw!important"alt='Open In Colab'></a>
<a href='https://mybinder.org/v2/gh/hno2/uff/HEAD?filepath=Beispiele.ipynb' target="_blank"><img src='/images/icons/binder-badge.svg' alt='Open In myBinder' style="width:10vw!important"></a>

## Was ist NLP?
Natural Language Processing, die Kunst natürliche Sprache in Computern verstehen.
## Was kann NLP?
* [Programmcode erzeugen und verstehen](https://copilot.github.com/)
* [Matheaufgaben lösen](https://openai.com/blog/grade-school-math/)
* und außerdem: [besser Übersetzen](https://www.deepl.com/), [(dadaistische) Texte schreiben](https://transformer.huggingface.co/), [Fragen anhand von Kontext beantworten](https://huggingface.co/deepset/roberta-base-squad2) auch [zu Tabellen](https://huggingface.co/google/tapas-base-finetuned-wtq) und [Spracherkennung](https://huggingface.co/facebook/wav2vec2-base-960h)
## Wie funktioniert NLP?
* Mit Machine Learning, welches die Abstraktion und Aneignung von abstrakten Wissen und Verständnis in Neuronalen Netzen mithilfe von Trainingsbeispielen beschreibt.
* Nahezu alle aktuellen (State of the Art) Ansätze basieren auf einer Architektur für Neuronale Netze namens *Transformers* [@@vaswani2017attention], die alle einen Attention-Mechanismus besitzen, die ihnen erlaubt ein Kontextverständnis auszubauen. Der *Encoder* setzt den *Input* in ein *Embedding* um, welches der *Decoder* wieder in Text (*Output*) übersetzt. Dies Architektur nennt man auch die Encoder-Decoder-Architecture oder seq-2-seq (Sequence to Sequence), da sie aus einem textuellen Input in einen textuellen Output erzeugt und wird z.B. für Übersetzungen genutzt.
* [Visualisierung des Attentionmechanismus](https://huggingface.co/exbert/?model=bert-base-german-cased&modelKind=bidirectional&sentence=Ich%20liebe%20dich%20weil%20du%20sch%C3%B6n%20bist.&layer=2&heads=..0,1,2,3,4,5,6,7,8,9,10,11&threshold=0.79&tokenInd=5&tokenSide=left&maskInds=..&hideClsSep=true) für deutsche Sätze.
* [Deutsches Bert Modell](https://huggingface.co/bert-base-german-cased)
* [Warum die Modelle nach der Sesamstraße (engl. Muppets) benannt sind](https://www.theverge.com/2019/12/11/20993407/ai-language-models-muppets-sesame-street-muppetware-elmo-bert-ernie)

Anstatt NLP-Modelle von Grund auf neu zu trainieren (was teuer ist und dauert), ist es jetzt möglich (und ratsam), vortrainierte Sprachmodelle zu nutzen, um gängige NLP-Aufgaben zu erfüllen. Viele der Modelle sind 
## Kann ich das Anwenden?
**Ja**, sogar komplett kostenlos - rudimentäre Python Kentnisse vorrausgesetzt. 

Das einfachste Beispiel ist *Sentiment Analysis*, bei Text nach Stimmung (positiv, negativ) klassifiziert wird. Auf Huggingface sind hierführ verschiedene Modelle mit unterschiedlicher Datengrundlage und Sprache verfügbar. Für die deutsche Sprache biete sich das Model [oliverguhr/german-sentiment-bert](https://huggingface.co/oliverguhr/german-sentiment-bert) von [@guhr2020training] an. Dieses wurde mit 1.834 millionen deutschen Beispielen unter anderem von Bewertungsplattformen trainiert. 
```py
from transformers import pipeline

classifier = pipeline("sentiment-analysis", model="oliverguhr/german-sentiment-bert")
texts = [
    "Mit keinem guten Ergebniss",
    "Das ist gar nicht mal so gut",
    "Naja, war ok",
    "Total toll!",
    "Nicht so schlecht wie erwartet",
    "Sie fährt ein grünes Auto.",
]
outputs = classifier(texts)

print(outputs)
```

## Zero-Shot Learning
* Zero-Shot Learning beschreibt das "Erlernen" von Fähigkeiten ohne Trainingbeispiele. Da die NLP-Netze immer besser darin werden, Sprache zu verstehen können diese auch Anweisungen in natürlicher Sprache verstehen
* Eine Kurzzusammenfassung zum n-shot learning finden sich in [diesem Blogpost](/uff)


```py
from transformers import pipeline
# Warning! This model is about 10GB in size!
generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')
prompt="""
Airport code extractor:
 
Text: "I want to fly form Los Angeles to Miami." 
Airport codes: LAX, MIA 

Text: "I want to fly from Orlando to Boston" 
Airport codes:"""
generator(prompt, do_sample=True, min_length=50)
```
Fast jedes Problem aus dem Bereich Machine Learning lässt sich als n-shot Problem beschreiben. Siehe dazu zum Beispiel [Prompt Source](https://github.com/bigscience-workshop/promptsource). N-Shot Learning ist aber schwieriger und somit oft weniger genau als der klassiche Machine Learning Ansatz mit Trainingsdaten. Wo zero-shot learning oft aber sehr gut funktioniert ist die Klassifizierung, hier an Beispielen von Zeitungsartikeln. 

```py
from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="Sahajtomar/German_Zeroshot")
sequences = [
    "Letzte Woche gab es einen Mord im nahe gelegenen Ort Unterweiler.",
    "Die meisten Menschen sind geimpft. Trotzdem steigen die Infektionsahlen. Soll ich noch auf eine Geburtstagsfeier oder Hochzeit gehen? Das raten Expertinnen und Experten.",
    "Letzes Jahr wurden 15% weniger Ladendiebstähle verübt.",
    "Am 19. Februar jährt sich der Anschlag in Hanau, bei dem neun Menschen mit Migrationshintergrund gezielt erschossen wurden.",
    "Ziel des  Handelns muss es sein, langfristig zu denken und ökonomische und ökologische Lösungen zu schaffen, die auch für künftige Generationen von Vorteil sind.",
]
candidate_labels = ["Verbrechen", "Krankheit", "Rassissmus", "Nachhaltigkeit"]
hypothesis_template = "In diesem geht es um {}."
outputs = classifier(
    sequences, candidate_labels, hypothesis_template=hypothesis_template
)
```

### NLP in der Bildung
* Kann [sinnvolles, individuelles Feedback](http://ai.stanford.edu/blog/prototransformer/) automatisieren, [Multiple Choice Fragen](https://link.springer.com/article/10.1007/s11042-021-11222-2) oder [Flashcard](https://psionica.org/tools/autocards/) generieren. Dies erlaubt neuartige Lehr- und Lernkonzepte oder die Skalierung Richtung MOOCs.