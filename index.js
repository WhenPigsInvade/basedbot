//mentioned.js needs fixing!!!
//TODO:
//Emojify script
//updating username if user changed it
//leaderboard formating
//channel renaming for swearword count
//nuke leaderboard


//Client Version:
const version = '1.1.2';

const Discord = require('discord.js');
const client = new Discord.Client();
//const token = ''; //For BasedBot
const token = ''; //For BasedBotBeta
const PREFIX = '&';
const fs = require('fs');




var userdata = require("./userdata.json");
var serverdata = require("./serverdata.json");

//For keyword leaderboard
client.usersettings = require("./userdata.json");

//For server settings
client.serversettings = require("./serverdata.json");

//create collection for commands
client.commands = new Discord.Collection();

const commandFiles = fs.readdirSync('./commands/').filter(file => file.endsWith('.js'));
for(const file of commandFiles){
    const command = require(`./commands/${file}`);

    client.commands.set(command.name, command);
    console.log('Commands loaded');
}

//create collection for replies
client.replies = new Discord.Collection();

const replyFiles = fs.readdirSync('./replies/').filter(file => file.endsWith('.js'));
for(const file of replyFiles){
    const reply = require(`./replies/${file}`);

    client.replies.set(reply.name, reply);
    console.log('Replies loaded');
}

//create collection for functions
client.leaderboard = new Discord.Collection();

const leaderboardFiles = fs.readdirSync('./leaderboard/').filter(file => file.endsWith('.js'));
for(const leaderboardFile of leaderboardFiles){
    const file = require(`./leaderboard/${leaderboardFile}`);

    client.leaderboard.set(file.name, file);
    console.log('Leaderboard and functions loaded');
}


//creat collection for keywords
client.keywords = new Discord.Collection();

const keywordFiles = fs.readdirSync('./leaderboard/').filter(file => file.endsWith('.js'));
for(const file of keywordFiles){
    const keyword = require(`./leaderboard/${file}`);

    client.keywords.set(keyword.name, keyword);
    console.log('Keywords loaded');
}


client.login(token);

var changed = false;

client.on('ready',() => {
    console.log('This bot is online!');
    console.log(`Current version ${version}`);
    // console.log(client.user.id);

    //Sets status
    const statusList = [
        `~help for more info!`,
        `~log for changes!`,
        `over ${client.guilds.cache.size} servers!`,
        `current version ${version}`
    ];

    let index = 0;
    setInterval(() => {
        if(index === statusList.length) index = 0;
        var status = statusList[index];
        client.user.setActivity(status, {type: "WATCHING"}).catch(console.error)
        index++;
    }, 5000)

    setInterval(() => {
        if(changed){
            fs.writeFile ("./userdata.json", JSON.stringify(client.usersettings,null,4), err => {
                if(err) throw err;
            });
            fs.writeFile ("./serverdata.json", JSON.stringify(client.serversettings,null,4), err => {
                if(err) throw err;
            });
        }
        changed = false;
    }, 1800000)
    
});






//COMMANDS
//PREFIX '~'
client.on('message', message => {

    if(!message.author.bot){


       

        //COMMANDS
        //
        //
        //
        //
        //


        //If command is called, it will not record chat
        if(message.content.charAt(0)===PREFIX.charAt(0)){ //Prefix is string, not char, so that's why we need.charAt()
            let args = message.content.substring(PREFIX.length).split(" ");

            switch(args[0]){

                // case 'username':
                //     message.channel.send(client.users.cache.get(message.author.id).tag);
                // break;

                case 'help':
                    client.commands.get('help').execute(message,args);
                break;

                case 'top':
                    client.leaderboard.get('top').execute(client,message,args[1],args[2],serverdata,userdata,Discord);
                break;

                case 'log':
                    client.commands.get('log').execute(message);
                break;

                // case 'clearartifacts':
                //     client.commands.get('clearartifacts').execute(userdata, message, fs, client);
                // break;

                case 'keywords':
                    switch(args[1]){
                        case 'add':
                            client.leaderboard.get('add').execute(message, args[2], serverdata, userdata, client, fs);
                        break;

                        case 'delete':
                            client.leaderboard.get('delete').execute(message, args[2], serverdata, userdata, client, fs);
                        break;

                        case 'reset':
                            client.leaderboard.get('reset').execute(message, args[2], serverdata, userdata, client, fs);
                        break;

                        default:
                            //Displays leaderboard for guild
                            client.leaderboard.get('keywords').execute(message, serverdata, Discord);
                    }

                break;

            }
        } else {

            if(client.leaderboard.get('logging').execute(message,client,serverdata,userdata,fs) == true) changed = true;
            

            //Other replies
            //
            //
            //
            //
            //
            // console.log(typeof(message));
            // console.log(message.toString().search(/\belliot\b/i));
            if((message.toString().search(/\belliot\b/i) !== -1) || (message.toString().search(/\beliott\b/i) !== -1)){
                client.replies.get('elliott').execute(message);
            }
            // console.log(message.toString().search(/\belliot\b/i) !== -1);
            // if(message.toString().search(/\belliot\b/i) !== -1){
            //     console.log();
            // }


            switch(message.content.toLowerCase()){
                case 'brb':
                    client.replies.get('brb').execute(message);
                    break;

                case 'f':
                    client.replies.get('f').execute(message);
                    break;
            }


            //When Based is mentioned
            //
            //
            //
            //
            //
            if(message.content.includes("@here") || message.content.includes("@everyone")){
                message.reply("Hey dumbass we're trying to sleep here.");
            } else if(message.mentions.users.has(client.user.id)){
                client.replies.get('mentioned').execute(message);
            }

        }
    }
})
