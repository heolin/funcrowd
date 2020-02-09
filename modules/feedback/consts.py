
class FeedbackTypes:
    NONE = "NONE"
    CONFIRM_ONLY = "CONFIRM_ONLY"
    BINARY = "BINARY"
    QUIZ = "QUIZ"
    QUESTIONNAIRE = "QUESTIONNAIRE"
    POINTS = "POINTS"
    NER = "NER"
    CLASSIFICATION = "CLASSIFICATION"


FEEDBACK_TYPES = (
    (FeedbackTypes.NONE, "None"),
    (FeedbackTypes.CONFIRM_ONLY, "Confirm only"),
    (FeedbackTypes.BINARY, "Binary"),
    (FeedbackTypes.QUIZ, "Quiz"),
    (FeedbackTypes.QUESTIONNAIRE, "Questionnaire"),
    (FeedbackTypes.POINTS, "Points"),
    (FeedbackTypes.NER, "NER"),
    (FeedbackTypes.CLASSIFICATION, "Classification")
)
