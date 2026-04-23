

Draft Document for Review December 11, 2019 1:55 pm                                                    8459ch06.fm

environment. The Master, Infrastructure and Compute Roles are deployed to a single node (Figure 6-1).

| Automation&#xA;CI/CD Tools	Cluster&#xA;Administrators	Developers	Application&#xA;Owners |   |   |   |
| --------------------------------------------------------------------------------------- | - | - | - |


</td>
<td rowspan="3"></td>
<td rowspan="3">

| ☺ ☺                                                                                                |   |   |   |   |
| -------------------------------------------------------------------------------------------------- | - | - | - | - |
| ☺ ☺ ☺                                                                                              |   |   |   |   |
| **Application Users**<br/>http\:/\<myapp>.ocp.example.com<br/>https\:/\<myapp>.ocp.example.com:443 |   |   |   |   |


</td>
</tr>
<tr>
<td colspan="4" style="text-align:center">↓ ↓ ↓ ↓</td>
</tr>
<tr>
<td colspan="4">

| **1** | **Web Console :8443** - - - - **Router :80 & :443 2 ←**        |   |   |
| ----- | -------------------------------------------------------------- | - | - |
|       | https\://ocp.example.com:8443                                  |   |   |
|       | POD&#xA;POD&#xA;POD&#xA;C	POD&#xA;POD&#xA;POD&#xA;C&#xA;3 PODs |   |   |


</td>
<td colspan="2" style="background-color:red; color:white"><b>REGISTRY</b></td>
</tr>
<tr>
<td colspan="2" style="background-color:red; color:white"><b>Jenkins</b></td>
</tr>
<tr>
<td>

| 🗄️ 🗄️ 🗄️ |                 |   |
| ----------- | --------------- | - |
| **4**       | **PVC Storage** |   |


</td>
<td colspan="2" style="background-color:red; color:white"><b>S2i</b></td>
</tr>
<tr>
<td></td>
<td></td>
<td colspan="2" style="background-color:red; color:white"><b>Prometheus</b></td>
</tr>
<tr>
<td></td>
<td></td>
<td colspan="2" style="background-color:red; color:white"><b>K8s Operators</b></td>
</tr>
<tr>
<td></td>
<td></td>
<td colspan="2" style="background-color:red; color:white"><b>OLM</b></td>
</tr>
<tr>
<td></td>
<td></td>
<td colspan="2" style="background-color:red; color:white"><b>............</b></td>
</tr>
</table>

</td>
</tr>
</table>

*Figure 6-1   OpenShift Container Platform 3.11 all-in-one*

* **Seven nodes deployment** is highly available and suitable for production. The Master and Infrastructure Roles are deployed to three Nodes, the Computer Role is deployed to three Worker Nodes, and the Load Balancer is deployed to a single Node (Figure 6-2).

| Automation&#xA;CI/CD Tools	Cluster&#xA;Administrators	Developers	Application&#xA;Owners	☺ ☺&#xA;☺ ☺ ☺&#xA;Application&#xA;Users	http\:/\<myapp>.ocp.example.com&#xA;https\:/\<myapp>.ocp.example.com:443 |   |   |   |   |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | - | - | - | - |


</td>
</tr>
<tr>
<td colspan="5" style="text-align:center">↓ ↓ ↓ ↓</td>
</tr>
<tr>
<td colspan="2">

| **Load Balancer \[LB]**    |                            |                            |
| -------------------------- | -------------------------- | -------------------------- |
| ↙ ↓ ↘                      |                            |                            |
| **Routers**                |                            |                            |
| **Master - Infra**<br/>🖥️ | **Master - Infra**<br/>🖥️ | **Master - Infra**<br/>🖥️ |
| **Registry**               |                            |                            |
| **1**                      | **Master Nodes**           |                            |


</td>
<td></td>
<td colspan="2">

| **APP<br/>POD<br/>POD<br/>C** | **APP<br/>POD<br/>POD<br/>C** | **APP<br/>POD<br/>POD<br/>C** |
| ----------------------------- | ----------------------------- | ----------------------------- |
| 🗄️ 🗄️ 🗄️                   |                               |                               |
| **PVC Storage**               |                               |                               |
| **2**                         | **Application Nodes**         |                               |


</td>
</tr>
</table>

*Figure 6-2   OpenShift Container Platform 3.11 6xNodes + Load Balancer*

Chapter 6. Installing Red Hat OpenShift 3.11 on IBM PowerVC       105
