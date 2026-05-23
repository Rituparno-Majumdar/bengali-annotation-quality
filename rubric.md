# Annotation Rubric: Bengali Sentiment Classification

**Dataset:** BLP-2023 Task 2 — Sentiment Analysis of Bangla Social Media Posts  
**Labels:** Positive | Negative | Neutral  
**Annotator:** Rituparno Majumdar (native Bengali speaker)

---

## Label Definitions

### Positive
The text expresses approval, happiness, praise, hope, agreement, or any favourable sentiment toward the subject.

Examples of Positive signals:
- Praise of a person, event, or outcome
- Expressions of gratitude or support
- Good news reported with approval
- Agreement or endorsement

### Negative
The text expresses disapproval, criticism, anger, sadness, fear, disgust, or any unfavourable sentiment toward the subject.

Examples of Negative signals:
- Criticism or condemnation of a person, policy, or event
- Expressions of frustration, outrage, or disappointment
- Bad news reported with negativity
- Sarcasm that conveys criticism (see edge cases below)

### Neutral
The text is factual, informational, or ambiguous with no clear emotional direction. The writer is reporting rather than evaluating.

Examples of Neutral signals:
- News headlines stating facts without editorial tone
- Questions without implied sentiment
- Mixed sentiment where no single polarity dominates
- Statements that could be read as either Positive or Negative without context

---

## Decision Rules

1. **Whole-text sentiment, not topic sentiment.** Label the writer's expressed sentiment, not whether the topic itself is good or bad. A factual report of a terrorist attack is Neutral, not Negative.

2. **Sarcasm defaults to Negative.** If a text uses positive words to mock or criticise, label it Negative. Mark it in annotation notes.

3. **Questions are usually Neutral** unless the phrasing clearly implies a positive or negative stance.

4. **Religious or political content:** Label based on the writer's expressed sentiment only. Do not apply personal judgement about the subject matter.

5. **Code-mixed text (Bengali + English):** Label the overall sentiment of the whole text. Mixed-script words are common in Bengali social media and do not affect the labelling process.

6. **When genuinely unsure between two labels:** Choose the one that best reflects the dominant tone. Record the item in your annotation notes as a borderline case.

---

## Label Distribution Target

The gold dataset slice is balanced: 50 Positive, 50 Negative, 50 Neutral.  
If your annotations deviate strongly from this distribution, review borderline cases before finalising.
