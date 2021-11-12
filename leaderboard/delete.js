module.exports = {
    name: 'delete',
    description: "delete keyword to word logger",
    execute(message, keyword, serverdata, userdata, client, fs){

        var index = serverdata[message.guild.id].keywords.indexOf(keyword)
        if(!message.guild.member(message.author).hasPermission('MANAGE_MESSAGES')){
            message.channel.send("Invalid permissions");

        } else if(keyword == null){
            message.channel.send("Invalid keyword");

        } else if(index !== -1){

            message.reply(`Are you sure you want to delete ${keyword}? This will delete keyword count for all users in this server and the word will no longer be logged. (y/n)`);

            message.channel.awaitMessages(confirmation => confirmation.author.id == message.author.id, {max: 1, time: 10000}).then(collected => {
                if(collected.first().content.toLowerCase() == 'y'){
                serverdata[message.guild.id].keywords.splice(index, 1);

                for(let userID of Object.keys(userdata[message.guild.id].users)){
                    userdata[message.guild.id].users[userID].count.splice(index, 1);
                    // console.log(userdata[message.guild.id].users[userID].count);
                }

                fs.writeFile ("./serverdata.json", JSON.stringify(client.serversettings,null,4), err => {
                    if(err) throw err;
                });

                fs.writeFile ("./userdata.json", JSON.stringify(client.usersettings,null,4), err => {
                    if(err) throw err;
                });

                message.channel.send(`${keyword} will no longer be logged.`);
                console.log(`User ${message.author.id} deleted ${keyword} logging in server ${message.guild.id}`);
        
                } else {
                    message.reply('Delete canceled.');
                }
            }).catch(() => {
                message.reply('Reset operation timed out.');
            });
            

        } else {
            message.channel.send(`${keyword} is not being logged right now.`);
        }


}}