module.exports = {
    name: 'clearartifacts',
    description: "clear any potential artifacts from previous updates",
    execute(userdata, message, fs, client){

    for(let userID of Object.keys(userdata[message.guild.id].users)){
        console.log(userdata[message.guild.id].users[userID].username);
        if(userdata[message.guild.id].users[userID].username){
            delete userdata[message.guild.id].users[userID].username;
        }   

    }
    fs.writeFile ("./userdata.json", JSON.stringify(client.usersettings,null,4), err => {
        if(err) throw err;
    });
}}