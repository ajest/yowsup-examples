# Yowsup Examples
A few examples for Yowsup library

# Stepts to use yowsup / aragurdev library

1.- You have to configure your number in a phone, install WhatsApp, send a few messages and recieve a few messages

2.- Search your Country Code (https://countrycode.org/)

3.- Search your MCC and MNC code (https://en.wikipedia.org/wiki/Mobile_country_code)

4.- In the terminal, inside yowsup folder, type the following command: yowsup-cli registration --requestcode sms --phone PHONE_NUMBER --cc COUNTRY_CODE --mcc MCC_CODE --mnc MNC_CODE

5.- After you receive the code in a text message (six numbers code), type the following command: yowsup-cli registration --register TEXT_MESSAGE_CODE --phone PHONE_NUMBER --cc COUNTRY_CODE

6.- Save the data that the command has returned in a file called "wasap_config.txt", specially the "login" and "pw" data, in this format: 
cc=COUNTRY_CODE
phone=PHONE_NUMBER
password=GIVEN_PASSWORD

7.- Execute the following command to enter in the Command line interface demo: yowsup-cli demos --config wasap_config.txt -y

8.- /login PHONE_NUMBER UvjH34odlO0ES7AhM45m3G57JV4=

9.- /message DESTINATION_NUMBER "Hola pablito!!"

10.- Another way to send a message is: yowsup-cli demos --config wasap_config.txt --send DESTINATION_NUMBER "Esto es asi, es simple"