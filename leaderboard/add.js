module.exports = {
    name: 'add',
    description: "add keyword to word logger",
    execute(message, keyword, serverdata, userdata, client, fs){

        if(!message.guild.member(message.author).hasPermission('MANAGE_MESSAGES')){
            message.channel.send("Invalid permissions");

        } else if(keyword == null){
            message.channel.send("Invalid keyword."); 
            
        } else if(serverdata[message.guild.id].keywords.indexOf(keyword) === -1){
            if(serverdata[message.guild.id].keywords.length < 10) {

                serverdata[message.guild.id].keywords.push(keyword);
                console.log(serverdata[message.guild.id].keywords);
                
                //Add the values for userdata
                for(let userID of Object.keys(userdata[message.guild.id].users)){
                    userdata[message.guild.id].users[userID].count.push(0);
                    // console.log(userdata[message.guild.id].users[userID].count);
                }
                
                fs.writeFile ("./serverdata.json", JSON.stringify(client.serversettings,null,4), err => {
                    if(err) throw err;
                });

                fs.writeFile ("./userdata.json", JSON.stringify(client.usersettings,null,4), err => {
                    if(err) throw err;
                });

                message.channel.send(`${keyword} is now being logged.`);
                console.log(`User ${message.author.id} added ${keyword} logging from server ${message.guild.id}`);
            } else {
                message.channel.send('Cannot log more than 10 keywords. Support BasedBot and its development by purchasing premium time to unlock more logs!')
            }

        } else {
            message.channel.send(`${keyword} is already being logged. Use parameter 'reset' to reseet word count.`);
        }


}}