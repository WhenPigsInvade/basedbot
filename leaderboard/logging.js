module.exports = {
    name: 'logging',
    description: "Keyword logger",
    execute(message,client,serverdata,userdata,fs){
        
        var changed = false;

        //Keyword logging
            //
            //
            //
            //
            //

        //Default words to check upon new server
        var keywords = [
            "fuck", 
            "ass",
            "bitch",
            "damn",
            "shit",
        ];

        //Finds guild and choose settings
        if(!serverdata[message.guild.id]){
            console.log(message.guild.id + " added to serverdata.json");
            let temp = [
                "fuck", 
                "ass",
                "bitch",
                "damn",
                "shit",
            ];
            serverdata[message.guild.id] = {
                keywords: temp,
            }

            changed = true;

            // fs.writeFile ("./serverdata.json", JSON.stringify(client.serversettings,null,4), err => {
            //     if(err) throw err;
            // });
        } else {
            //If server setting is availible, load settings
            keywords = serverdata[message.guild.id].keywords;
        }



        for(var i = 0; i < keywords.length; i++){
            var regex = new RegExp("\\b"+keywords[i]+"\\b", "i");
            if(message.toString().search(regex) !== -1){

                //If guild isn't inside userdata, make a new object for said guild
                if(!userdata[message.guild.id]){
                    //make arraylist that stores count for all users
                    console.log("New guild recorded: " + message.guild.id);
                    
                    let tempCount = new Array();
                    for(let j = 0;j<keywords.length;j++){
                        if(i == j){
                            //User just said keyword
                            tempCount.push(1);
                        } else {
                            tempCount.push(0);
                        }
                    }

                    let tempUser = new Object();
                    tempUser[message.author.id] = {
                        count: tempCount,
                        // username: message.author.tag,
                    }

                    userdata[message.guild.id] = {
                        users: tempUser,
                    }
                    console.log(userdata[message.guild.id]);

                    // userdata[message.guild.id].user[message.author.id] = {
                    //     count: tempCount,
                    //     username: message.author.tag,
                    // };


                    
                } else {
                    //If guild is on record, we need to then check is user is on record or not

                    if(userdata[message.guild.id].users[message.author.id]){
                        // console.log('user exists')
                        userdata[message.guild.id].users[message.author.id].count[i] ++;

                        // if(userdata[message.guild.id].users[message.author.id].username) removePro;
                    } else {
                        // console.log('user doesn\'t exists')

                        let tempCount = new Array();
                        for(let j = 0;j<keywords.length;j++){
                            if(i == j){
                                //User just said keyword
                                tempCount.push(1);
                            } else {
                                tempCount.push(0);
                            }
                        }

                        let tempUser = new Object();

                        userdata[message.guild.id].users[message.author.id] = {
                            count: tempCount,
                            // username: message.author.tag,
                        }

                        


                    }


                    // let temp = userdata[message.author.id].count;
                    // let fullusername = userdata[message.author.id].username;
                    // temp[i] = temp[i]+1;
                    // userdata[message.author.id] = {
                    //     count: temp,
                    //     username: fullusername
                    // };
                }

                //writes to json
                // fs.writeFile ("./userdata.json", JSON.stringify(client.usersettings,null,4), err => {
                //     if(err) throw err;
                // });

                changed = true;
            }
        }
        return changed;
    }
}