const express = require("express");
const multer = require("multer");
const bodyParser = require("body-parser");

const app = express();
const port = process.env.PORT || 3000;
app.use(bodyParser.urlencoded({ extended: false }));
// Configure multer for file uploads
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });
// Serve static files (uploaded files)
app.use("/uploads", express.static("uploads"));
app.get("/", (req, res) => {
  res.send("Welcome to the file upload app!");
});
// Sample route to handle file uploads
app.post("/upload", upload.single("file"), async (req, res) => {
  try {
    const file = req.file;

    if (!file) {
      return res.status(400).send("No file uploaded.");
    }

    // Here, you can save the file to Google Drive or any other cloud storage
    // and generate a link to it.
    res.status(200).send("File uploaded successfully.");
  } catch (error) {
    console.error(error);
    res.status(500).send("An error occurred.");
  }
});
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
