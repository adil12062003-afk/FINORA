from pathlib import Path
import re
files=list(Path("android/app/src/main/java").rglob("MainActivity.java"))
if not files: raise SystemExit("MainActivity.java not found after cap add android")
p=files[0]; s=p.read_text()
if "ModifiedMainActivityForSocialLoginPlugin" in s: raise SystemExit(0)
package=re.search(r"^package\s+([\w.]+);",s,re.M)
if not package: raise SystemExit("Could not detect MainActivity package")
new=f'''package {package.group(1)};

import android.content.Intent;
import android.util.Log;
import com.getcapacitor.BridgeActivity;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginHandle;
import ee.forgr.capacitor.social.login.GoogleProvider;
import ee.forgr.capacitor.social.login.SocialLoginPlugin;
import ee.forgr.capacitor.social.login.ModifiedMainActivityForSocialLoginPlugin;

public class MainActivity extends BridgeActivity implements ModifiedMainActivityForSocialLoginPlugin {{
  @Override
  public void onActivityResult(int requestCode, int resultCode, Intent data) {{
    super.onActivityResult(requestCode, resultCode, data);
    if (requestCode >= GoogleProvider.REQUEST_AUTHORIZE_GOOGLE_MIN && requestCode < GoogleProvider.REQUEST_AUTHORIZE_GOOGLE_MAX) {{
      PluginHandle handle = getBridge().getPlugin("SocialLogin");
      if (handle == null) {{ Log.i("Google Activity Result", "SocialLogin handle is null"); return; }}
      Plugin plugin = handle.getInstance();
      if (plugin instanceof SocialLoginPlugin) ((SocialLoginPlugin) plugin).handleGoogleLoginIntent(requestCode, data);
    }}
  }}
  @Override public void IHaveModifiedTheMainActivityForTheUseWithSocialLoginPlugin() {{}}
}}
'''
p.write_text(new)
