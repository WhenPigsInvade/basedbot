const messages = [
    "Ok, I'm in.", 
    "Nope. My log is too big :/"
];
module.exports = {
    name: 'log',
    description: "Shows changelog",
    execute(message){
    

        // message.delete({timeout:2000});

        if(Math.random() > 0.5 && message.guild.me.hasPermission("MANAGE_MESSAGES")) {
            message.delete();
        } else {
            message.channel.send("Fitting my log in your ass...");
            setTimeout(function(){ message.channel.send(messages[Math.floor(Math.random() * messages.length)]) }, 3000);
        }
}}