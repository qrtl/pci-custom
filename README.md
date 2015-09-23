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
<h3>2. Enabling physical inventories with a past date</h3>
<p>Follow below steps for the preparation of applying bug fix/enhancement on physical inventories.</p>
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
        <p>Install <code>stock_physical_inventory_adjust</code>.</p>
    </li>
</ol>
<h1>Changes Made to OpenERP By This Extension</h1>
<ol>
    <li>
        <p><code>Creation Date</code></p>
        <ol>
            <li>
                <p>This date will have no substantial impact for stock move an journal entry records. Please use this date just for reference.<p>
            </li>
        </ol>
    </li>
    <li>
        <p><code>Date Done</code></p>
        <ol>
            <li>
                <p>At <code>Confirm Inventory</code> OpenERP does following calculation to generate stock move records:</p>
                <p>(<code>Quantity</code> in <code>General Information</code> tab) &minus; (<code>Quantity</code> as of <code>Date Done</code>)</p>
            </li>
            <li>
                <p>At <code>Validate Inventory</code> the <code>Date Done</code> value is used as the effective date for stock moves and associated journal entry.</p>
            </li>
        </ol>
    </li>
</ol>
<h1>Some Points to Note</h1>
<ol>
    <li>
        <p>When one presses <code>Fill Inventory</code>, OpenERP populates <code>General Information</code> tab with products and quantities. The info is based on the current OpenERP inventory, not the inventory as of <code>Creation Date</code> or <code>Date Done</code>. <strong>This is the default behavior of OpenERP.</strong></p>
    </li>
    <li>
        <p>When one presses <code>Validate Inventory</code>, OpenERP generates a journal entry while changing the status of stock moves to <code>Done</code>. However, when one presses <code>Cancel Inventory</code>, OpenERP does not cancel the corresponding journal entry. <strong>This is a bug, but is on the roadmap to be fixed. Please, remember to delete the journal entry if <code>Cancel Inventory</code> is used.</strong></p>
    </li>
    <li>
        <p>Since we have modified the original <code>stock.py</code> file, if one updates OpenERP, depending on the latest source code changes to the <code>stock.py</code> file, the changes will need to be merged.</p>
    </li>
</ol>
