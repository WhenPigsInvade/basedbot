const messages = [
    "how'd you like that ping? No? Get off my screen.", 
    "nobody likes being pinged, so fuck off.",
    "since you like pinging me so much, lets play a little game. Stick one finger in your mouth, and another in your ass. Now switch!"
];
module.exports = {
    name: 'mentioned',
    description: "displays list of commands",
    execute(message){
        const randomMessage = messages[Math.floor(Math.random() * messages.length)];
        message.reply(randomMessage);
}}