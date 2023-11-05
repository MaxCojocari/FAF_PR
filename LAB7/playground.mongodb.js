/* global use, db */
// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

// The current database to use.
use("lab7");

// Clear contents of collection
// db.getCollection("lab7_collection").deleteMany({});

// Search for documents in the current collection.
db.getCollection("lab7_collection").find();
