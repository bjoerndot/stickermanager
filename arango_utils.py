import pyArango.connection as arang

DB = None

def errorDocNotFound(key):
    message = "Document {} was not found!".format(key)
    raise RuntimeError(message)

def connectToDB(DBName):
    # initialize Database (arango)
    connection = arang.Connection(arangoURL="http://192.52.32.248:8529", username="root", password="deermaester")
    global DB
    DB = connection[DBName]

def aqlDatabase(query, variableDict):
    global DB
    queryResult = DB.AQLQuery(query, bindVars = variableDict)
    return queryResult

def loadCollection(collectionName):
    collection = DB[collectionName]
    return collection

def checkDocument(collectionName, docKey):
    """
    Return Boolean

    collectionName = String
    docKey = String
    """
    collection = loadCollection(collectionName)
    allDocs = collection.fetchAll()
    existent = False
    for doc in allDocs:
        if doc["key"] == docKey or doc["id"] == docKey:
            existent = True
    return existent

def createDocument(collectionName, newDoc):
    if "key" in newDoc:
        docKey = newDoc["key"]
    else:
        raise RuntimeError("'key' was not submitted in dict")
        return False
    if checkDocument(collectionName, docKey):
        message = "A document with the key ({}) already exists. Therefore it can't be created.".format(docKey)
        raise RuntimeError(message)
        return False

    collection = loadCollection(collectionName)
    document = collection.createDocument()

    for k,v in newDoc.items():
        document[k] = v

    document._key = docKey
    document.save()
    return True

def getDocument(collectionName, docKey):
    collection = loadCollection(collectionName)
    if not checkDocument(collectionName, docKey):
        errorDocNotFound(docKey)
        return False
    document = collection[docKey]
    return document

def updateDocument(collectionName, updDoc, docKey):
    document = getDocument(collectionName, docKey)
    for k, v in updDoc.items():
        document[k] = v
    document.save()
    return True

def getStoredDocument(collectionName, docKey):
    document = getDocument(collectionName, docKey)
    document = document.getStore()
    return document

def fetchAllDocuments(collectionName):
    collection = loadCollection(collectionName)
    return collection.fetchAll()

def deleteDocument(collectionName, docKey):
    document = getDocument(collectionName, docKey)
    document.delete()
    return True

def getStored(doc):
    return doc.getStore()

def patchDocument(collectionName, updDoc, docKey):
    document = getDocument(collectionName, docKey)
    for k, v in updDoc.items():
        document[k] = v
    document.patch()
