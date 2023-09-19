// firebase-admin.js

const admin = require("firebase-admin");

const serviceAccount = require("./aerobic-cyclist-351707-firebase-adminsdk-yr37z-eb67fc1857.json");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});

module.exports = admin;
