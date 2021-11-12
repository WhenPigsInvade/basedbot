module.exports = {
    name: 'keywords',
    description: "displays list of keywords being logged",
    execute(message, serverdata, Discord){

        const list = new Discord.MessageEmbed()
                .setColor('#ff0000')
                .setTitle("Keywords")
                .setDescription("List of keywords logged by BasedBot")
                .setFooter(`Requested by ${message.author.tag}\nWant to increase log slots? Support BasedBot and its development by purchasing premium time to unlock more logs!`);

        let keywords = "";
        for(var i = 0; i < serverdata[message.guild.id].keywords.length; i++){
            keywords += serverdata[message.guild.id].keywords[i]+"\n";
        }
        
        list.addField(keywords, "\u200B", false);
        message.channel.send(list);

}}