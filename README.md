<h1>OpenERP 7.0 Reporting Customization</h1>
<p>The purpose of this is to extend the capabilities of OpenERP's abilities to report accounting and finances. By default OpenERP can export reports based on international accounting and financial standards, but the United States needs further options to
    allow easy reporting. To achieve this we utilize <a href="https://github.com/jamotion/aeroo">Aeroo Reports for OpenERP / Odoo 8.0</a> and also a custom <code>stock.py</code>.</p>
<h1>Installaton</h1>
<h3>1. Releasing customized financial reports</h3>
<p>Please follow below steps for the installation of the customized financial reports.</p>
<ol>
    <li>
        <p>Install required packages and OpenOffice (about 400MB disk space is required):</p>
        <pre><code>sudo apt-get install openoffice.org python-genshi python-cairo python-openoffice python-lxml python-uno</code></pre>
    </li>
    <li>
        <p>Get Aeroo Reports Library and install it as a Python module</p>
        <ol>
            <li>Move to your download directory.</li>
            <li>
                <p>Download Aeroo Reports using bazaar:</p>
                <pre><code>bzr branch lp:aeroolib</code></pre>
            </li>
            <li>
                <p>Change directory into the extension:</p>
                <pre><code>cd aeroolib/aeroolib</code></pre>
            </li>
            <li>
                <p>Install the python package:</p>
                <pre><code>sudo python ./setup.py install</code></pre>
            </li>
        </ol>
    </li>
    <li>
        <p>OpenOffice related setup</p>
        <ol>
            <li>
                <p>Create an OpenOffice init script</p>
                <ol>
                    <li>
                        <p>Create the file:</p>
                        <pre><code>sudo nano /etc/init.d/office</code></pre>
                    </li>
                    <li>
                        <p>Paste this:</p>
                        <pre><code>#!/bin/sh
/usr/bin/soffice --nologo --nofirststartwizard --headless --norestore --invisible "--accept=socket,host=localhost,port=8100,tcpNoDelay=1;urp;" &</code></pre>
                    </li>
                    <li>
                        <p>Make the file executable:</p>
                        <pre><code>sudo chmod +x /etc/init.d/office</code></pre>
                    </li>
                    <li>
                        <p>Add the script to startup:</p>
                        <pre><code>sudo update-rc.d office defaults</code></pre>
                    </li>
                </ol>
            </li>
            <li>
                <p>Test OpenOffice</p>
                <ol>
                    <li>
                        <p>Start the script:</p>
                        <pre><code>sudo /etc/init.d/office</code></pre>
                    </li>
                    <li>
                        <p>Test the connection:</p>
                        <pre><code>telnet localhost 8100</code></pre>
                        <p>If you see an output like below OpenOffice should be working:</p>
                        <pre><code>Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
eø–'com.sun.star.bridge.XProtocolPropertiesUrpProtocolProperties.UrpProtocolPropertiesTidgÕ„</code></pre>
                    </li>
                </ol>
            </li>
        </ol>
    </li>
    <li>
        <p>Install custom modules from GitHub.</p>
        <p><strong>Please note that we have added custom functionality to the original Aeroo Reports modules so the customized report functions could work.</strong></p>
        <ol>
            <li>
                <p>Move to your download directory.</p>
            </li>
            <li>
                <p>Clone the repository:</p>
                <pre><code>git clone https://github.com/rfhk/cip-customization.git</code></pre>
            </li>
            <li>
                <p>Add the cloned repository to your OpenERP addons.</p>
            </li>
            <li>
                <p>Restart OpenERP.</p>
            </li>
        </ol>
    </li>
    <li>
        <p>Update the module list in OpenERP</p>
    </li>
    <li>
        <p>Install each module: <code>report_aeroo</code>, <code>report_aeroo_ooo</code>, <code>account_financial_report_comparison</code>.</p>
    </li>
    <li>
        <p>Upon module installation, three menu items are added under <code>Accounting > Reporting > Legal Reports > Accounting Reports</code>.</p>
        <img>
    </li>
</ol>
<h3>2. Releasing customized financial reports</h3>
<p>Please follow below steps for the preparation of apply bug fix on physical inventory.</p>
<ol>
    <li>
        <p>Stop OpenERP.</p>
    </li>
    <li>
        <p>Replace <code>addons/stock/stock.py</code> with the <code>stock.py</code> file from the GitHub repository.</p>
    </li>
    <li>
        <p>Restart OpenERP.</p>
    </li>
    <li>
        <p>Through the frontend login and enter "Developer Mode" by clicking <code>User > About OpenERP > Activate the developer mode</code>.</p>
    </li>
    <li>
        <p>Navigate to <code>Physical Inventories</code> by going to <code>Warehouse > Inventory Control > Physical Inventories</code> and clicking the <code>Create</code> button.</p>
    <li>
        <p>Click <code>Debug View</code> dropdown and select <code>Edit FormView</code>.</p>
        <img>
    </li>
    <li>
        <p>Update the <code>FormView</code> to allow the visibility of field <code>date_done</code>:</p>
        <p>Place <code>&lt;field name="date_done"/&gt;</code> after line 21, below <code>&lt;field name="date"/&gt;</code></p>
        <img>
        <pre><code>&lt;group&gt;
    &lt;field name="date"/&gt;
    &lt;field name="date_done"/&gt;
    &lt;field name="company_id" groups="base.group_multi_company" widget="selection"/&gt;
&lt;/group&gt;</code></pre>
    </li>
    <li>
        <p>Refresh the page.</p>
    </li>
</ol>
<h1>Changes Made to OpenERP By This Extension</h1>
<ol>
    <li>
        <p><code>Creation Date</code> field:</p>
        <ol>
            <li>
                <p>This date will have no substantial impact for stock move an journal entry records. Please use this date just for reference.<p>
            </li>
        </ol>
    </li>
    <li>
        <p><code>Date Done</code> field:</p>
        <ol>
            <li>
                <p>We have added this field to take care of the following:</p>
                <ol>
                    <li>
                        <p>At <code>Confirm Inventory</code>:</p>
                        <ol>
                            <li>
                                <p>The system does following calculation to generate stock move records:</p>
                                <ol>
                                    <li>
                                        <p>(product qty in ‘General Information’ tab) - (product qty as of ‘Date Done’)</p>
                                    </li>
                                </ol>
                            </li>
                        </ol>
                    </li>
                    <li>
                        <p>At <code>Validate Inventory</code>:</p>
                        <ol>
                            <li>
                                <p>The <code>Date Done</code> value is used as the effective date for stock moves and associated journal entry</p>
                            </li>
                        </ol>
                    </li>
                </ol>
            </li>
        </ol>
    </li>
</ol>
<h1>Some Points to Note</h1>
<ol>
    <li>
        <p>When you press ‘Fill Inventory’, the system populates ‘General Information’ tab with products and quantities.  The info is based on the current system inventory (not the inventory as of ‘Creation Date’ or ‘Date Done’) &rarr; This is the behavior of the standard OpenERP.</p>
    </li>
    <li>
        <p>When you press ‘Validate Inventory’, the system generates a journal entry while changing the status of stock moves to ‘Done’.  However, when you press ‘Cancel Inventory’, the system does not cancel the corresponding journal entry &rarr; This should be a bug but we did not get to take care of this. Please set up the manual process of deleting the journal entry in case you do the ‘Cancel Inventory’ operation.</p>
    </li>
    <li>
        <p>Since we have modified the original stock.py file, in case you replace the whole set of OpenERP source code with a newer version in the future, you may need to apply the same (or similar - depending on the latest source code) changes to the stock.py file. We will support the code update if needed (it may take us several hours for checking, coding and testing).</p>
    </li>
</ol>
