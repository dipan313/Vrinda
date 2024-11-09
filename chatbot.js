require("dotenv").config();

// const {
//   GoogleGenerativeAI,
//   HarmCategory,
//   HarmBlockThreshold,
// } = require("@google/generative-ai");

const { GoogleGenerativeAI } = require("@google/generative-ai");
const genAI = new GoogleGenerativeAI(process.env.GEMINI_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });


const chat = model.startChat({
  history: [
    {
      role: "user",
      parts: [{ text: "Hello" }],
    },
    {
      role: "model",
      parts: [{ text: "Great to meet you. What would you like to know?" }],
    },
  ],
});
let result = chat.sendMessage("I have 2 dogs in my house.");
console.log(result.response.text());
result = await chat.sendMessage("How many paws are in my house?");
console.log(result.response.text());

























// const generationConfig = {
//   temperature: 0.9,
//   topP: 1,
//   maxOutputTokens: 2048,
//   responseMimeType: "text/plain",
// };

// async function run() {
//   const chatSession = model.startChat({
//     generationConfig,
//     history: [],
//   });

//   const result = await chatSession.sendMessage(
//     "What is the cure of Corn_(maize)___Cercospora_leaf_spot_Gray_leaf_spot"
//   );
//   console.log(result.response.text());
// }

// run();
