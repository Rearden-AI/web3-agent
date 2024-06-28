class TransactionsErrors:
    TRANSACTION_NOT_FOUND = "Transaction not found"
    TRANSACTION_ALREADY_EXISTS = "Transaction already exists"
    TRANSACTION_NAME_REQUIRED = "Transaction name is required"
    TRANSACTION_NAME_NOT_UNIQUE = "Transaction name is not unique"
    TRANSACTION_ID_REQUIRED = "Transaction id is required"
    TRANSACTION_DESCRIPTION_REQUIRED = "Transaction description is required"


class ChatErrors:
    GOOGLE_API_RESOURCE_EXHAUSTED = "Google API quota limits reached"


class Errors:
    transactions = TransactionsErrors()
    chats = ChatErrors()


errors = Errors()
