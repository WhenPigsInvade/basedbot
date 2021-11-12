const authorID = "241399479784177664";
const messages = [
    "Yup, you need to get some help.", 
    "Are you trolling or are you just stupid?", 
    "Did your mother drop you as a child?", 
    "Please stop asking me", 
    "Try Googling it. Oh nevermind I forgot you're too poor for Internet.",
    "Do you want me to call mommy?",
    "here try this: https://www.google.com/search?q=plastic+surgery+near+me"
];
module.exports = {
    name: 'help',
    description: "displays list of commands",
    execute(message,args){
        if(message.author.id === authorID){
            message.channel.send(
                "~help\n" + 
                "~keywords [keyword]\n" + 
                "~ping\n\n" +
                

                "Or type\n\n" +
                "brb\n" +
                "f\n" +
                "more commands will come in the future." 
            );
        } else {
            const randomMessage = messages[Math.floor(Math.random() * messages.length)];
            message.channel.send(randomMessage);
        }
    }
}