

The content of the welcome message is helpful when you need to notify users about some important information about the system, such as security warnings or a location description. To define and enable the welcome message by using the GUI, edit the text area with the message content and click **Save** (see Figure 5-80).

Figure 5-80 shows the configuration screen for enabling the login message.

The screen is divided into sections: Login (with General) and Login Message.

Under Login Message, the description reads: "The login message will be displayed to anyone logging into the GUI or in a CLI session."

The checkbox for "Login message:" is checked, indicating it is Enabled.

The text area contains the message: "This is an ITSO-managed system. Unauthorized access is restricted."

Buttons visible are Save and Reset.

Figure 5-80 Enabling login message

The resulting log-in screen is shown in Figure 5-81.

![](5fb340ad68b0c71df0b56698b137e35b_img.jpg)

Figure 5-81 shows the Storwize V7000 Storage Management login screen (ITSO\_V7000G2\_A).

The screen displays input fields for Username and Password, and a Sign In button.

A banner message is displayed below the input fields, highlighted by a red oval: "This is an ITSO-managed system. Unauthorized access is restricted."

Figure 5-81 Welcome message in GUI

The banner message also appears in the CLI login prompt window, as shown in Figure 5-82.

```
10.18.228.64 - PuTTY
login as: ITSO admin
This is an ITSO-managed system. Unauthorized access is restricted. Using keyboard-interactive authentication.
Password: [REDACTED]
```

Figure 5-82 Banner message in CLI