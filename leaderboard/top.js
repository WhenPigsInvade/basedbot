const { DiscordAPIError } = require("discord.js");

module.exports = {
    name: 'top',
    description: "displays leaderboard",
    execute(client,message,keyword,page,serverdata,userdata,Discord){
        console.log(`Leaderboard called in ${message.guild.id} by user ${message.author.id}`);
        // console.log(client.users.fetch(client.id).tag);

        async function getUsername(ID){
            let usr = await client.users.fetch(ID);
            // console.log("getUsername inquiry with ID: "+ID);
            // console.log("getUsername responded with username: "+usr.tag);
            // console.log(leaderboard);
            return usr.tag;
            // return client.users.fetch(ID);
        }
        

        // message.channel.send(client.users.cache.get(message.author.id).tag);

        let text = "";

        let keywords = serverdata[message.guild.id].keywords;
        let index = keywords.indexOf(keyword);
        if(index!==-1){

            text+="**" + serverdata[message.guild.id].keywords[index] + "**\n";

            //List of top ten users in server
            var leaderboard = [];
            var usernames = [];
            // leaderboard[0] = [0,0];
            
            // leaderboard[1] = 0;
            // console.log('length: ' + leaderboard.length);
            
            // //Sets every index in leaderboard to 0
            // for(let i = 0; i < leaderboard.length; i++){
                //     leaderboard[i] = 0;
                // }
                
                
            for(let userID of Object.keys(userdata[message.guild.id].users)){
                // console.log(userID);
                // console.log(client.users.cache.get(userID).tag);
                
                
                if(userdata[message.guild.id].users[userID].count[index] !== 0){
                    
                    let username = getUsername(userID);
                    usernames.push(username);
                    leaderboard.push(userdata[message.guild.id].users[userID].count[index]);
                    




                }
            }
            
            

            Promise.all(usernames).then(users => {
                // console.log(leaderboard);
                // console.log('All done');
                // console.log(users);

                for(let i = 0; i < leaderboard.length; i++){
                    leaderboard[i] = [leaderboard[i], users[i]];
                }
                
                leaderboard.sort((a,b) => {
                    if(a[0] === b[0]){
                        return 0;
                    }
                    else {
                        return (a[0] > b[0]) ? -1 : 1;
                    }
                });
                
                // console.log('all done with sort');
                // console.log(leaderboard);

                //Prints it in Discord

                const board = new Discord.MessageEmbed()
                .setColor('#ff0000')
                .setTitle(keyword)
                .setDescription(`Top usage for the word ${keyword}`)
                .setFooter(`Requested by ${message.author.tag}`);

                let count = 0;
                while(leaderboard[count] && count < 10){
                    board.addField(`${count+1}. ${leaderboard[count][1]}`, leaderboard[count][0], false);
                    count++;
                }

                message.channel.send(board);
                





                // let count = 0;
                // while(leaderboard[count] && count < 10){
                //     let temp = leaderboard[count][1];
                //     // text+= (count+1) + ". ";
                //     text+= leaderboard[count][0]
                //     for(let i =temp.length; i < 66;i++){
                //         text+="-";
                //     }
                //     text+= temp +"\n";
                //     count++;
                // }
                // console.log(text);
                // message.channel.send(text);


            }).catch((error) => {
                console.log('Promises fullfilled with error(s)');
                console.log(error.message);
                // console.log(users);
            });



            //Removes all 0 at the ends
            // if(leaderboard[leaderboard.length - 1] === 0) leaderboard.pop();
            // console.log(leaderboard);
            
            // if(idLeaderboard[idLeaderboard.length - 1] === 0) idLeaderboard.pop();
            // console.log(idLeaderboard);
            




            // let usernameList = new Array();
            // for(let j = 0; j < idLeaderboard.length; j++){
            //     // let temp = await client.users.fetch(idLeaderboard[j]);
            //     // usernameList.push(temp);
            //     client.users.fetch(idLeaderboard[j]).then(user => {
            //         console.log(user.tag + idLeaderboard[j]);
            //         usernameList[usernameList.length] = user.tag;
            //         console.log(usernameList);
            //     }).then( ()=> {
            //         console.log(usernameList);
            //     }).catch(err => {
            //         err.message;
            //     });
            // }
            // console.log(usernameList.toString);
            // console.log(usernameList.length);





            
            // client.users.fetch(idLeaderboard[0]).then((user) => {
            //     console.log(user.tag)});

            
            //Begin printing message



            
        } else {
            message.channel.send("Invalid argument");

        }
        
    }
}