<h1>WiFi Connection Checker and Restarter</h1>

<h2>Overview</h2>
<p>This Python script is designed to check the status of your WiFi connection on a Windows system. If the WiFi network is inactive and not able to receive ping packets, the script will automatically turn off the WiFi, turn it on again, and check whether the connection is live again or not. The script utilizes the <code>schedule</code> package for task scheduling, <code>netsh</code> commands for controlling the WiFi interface, and the <code>netifaces</code> package to retrieve meaningful network interface names.</p>

<h2>Prerequisites</h2>
<ul>
    <li>This script is specifically designed for Windows systems.</li>
    <li>The script requires administrative privileges to perform actions like turning off and on the WiFi interface.</li>
</ul>

<h2>Dependencies</h2>
<p>Install the <code>schedule</code> and <code>netifaces</code> packages using the following commands:</p>
<pre>
pip install schedule
pip install netifaces
</pre>

<h2>Usage</h2>
<ol>
    <li>Run the script with administrative privileges to ensure it can control the WiFi interface.</li>
    <pre>python wifi_checker.py</pre>
    <li>The script will schedule a periodic check of the WiFi connection status.</li>
    <li>If the WiFi connection is inactive (unable to receive ping packets), the script will automatically turn off and on the WiFi interface.</li>
    <li>The script will log the status of the WiFi connection in the console.</li>
</ol>

<h2>Important Notes</h2>
<ul>
    <li>Ensure that the script is run with administrative privileges to avoid permission issues.</li>
    <li>The script uses the <code>netsh</code> command to control the WiFi interface. If there are any issues with the execution of <code>netsh</code>, the script may not work as expected.</li>
</ul>

<h2>References</h2>
<ul>
    <li><a href="https://schedule.readthedocs.io/en/stable/" target="_blank">Schedule Package Documentation</a></li>
    <li><a href="https://stackoverflow.com/questions/373335/how-do-i-get-a-cron-like-scheduler-in-python" target="_blank">Stack Overflow: How do I get a cron-like scheduler in Python?</a></li>
    <li><a href="https://stackoverflow.com/questions/44246527/turn-wifi-off-using-python-on-windows-10" target="_blank">Stack Overflow: Turn WiFi off using Python on Windows 10</a></li>
    <li><a href="https://stackoverflow.com/questions/29913516/how-to-get-meaningful-network-interface-names-instead-of-guids-with-netifaces-un" target="_blank">Stack Overflow: How to get meaningful network interface names instead of GUIDs with netifaces?</a></li>
    <li><a href="https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script" target="_blank">Stack Overflow: Request UAC elevation from within a Python script</a></li>
</ul>

</body>
</html>
<!-- Updated README links and corrected typos -->
<!-- Updated README links and corrected typos -->