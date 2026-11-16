# FINORA — Android APK build package

FINORA is an offline-first personal finance record keeper. This package wraps the existing FINORA v1.0 HTML app in a native Android shell using Capacitor and builds a **debug APK** with GitHub Actions.

## Included features

- Separate cash and online balances
- Income, expenses, food & drinks category/ledger
- Game earnings, trading profit/loss, cashback and salary entries
- Udhaar given and taken, including partial repayments and a confirmation prompt
- Transaction history, reports, CSV export, JSON backup and restore

## Important data note

The current app stores records in browser-style local storage on the device. Export a JSON backup regularly. This is not bank/UPI/broker synchronization, and the debug APK is not a Play Store release build.

## Build your APK using GitHub (phone-friendly steps)

1. Extract this ZIP on your phone or computer.
2. Open GitHub and create a **new empty repository** named `FINORA` (do not add a README or license there).
3. Upload the **contents** of this extracted folder to the repository root. Make sure `.github/workflows/build-apk.yml` is included. If uploading through the GitHub website, enable viewing hidden files or create the workflow file/folders manually if `.github` is hidden by your file manager.
4. Open the repository's **Actions** tab.
5. Select **Build FINORA Android APK** and tap **Run workflow**. A push to `main` or `master` also starts a build automatically.
6. Wait until the workflow run shows a green check. Open that run, scroll to **Artifacts**, and download `FINORA-debug-apk`.
7. Extract the downloaded artifact ZIP. It contains `app-debug.apk`. Open it on your Android phone and follow Android's install prompt. Only install APKs from your own repository/build.

## What this build does and does not do

- GitHub Actions generates the Android project, installs Capacitor, and compiles the debug APK.
- No signing key is needed for this debug APK.
- A signed release APK/AAB for Play Store distribution needs a private signing key and a separate release configuration. Do not share that key in chat or commit it to the repository.
- This environment did not compile or install the APK. The APK is produced only after the GitHub Actions workflow completes successfully.

## Financial calculation rules checked in the current source

- Lending: subtract original principal from the selected cash/online balance.
- Receiving a repayment on a loan given: add the confirmed payment to the selected cash/online balance.
- Borrowing: add original principal to the selected cash/online balance.
- Repaying a loan taken: subtract the confirmed payment from the selected cash/online balance.
- Pending loan balance is original principal less confirmed repayments.

Please test with small sample amounts before entering real records. Keep a backup before updating the app.


## Google Drive integration setup (required before testing sign-in)

FINORA now includes an account-separated Drive sync interface using the Google Drive `appDataFolder` scope. Each Google account has its own private app-data area; the app stores each account's local ledger under a separate local key. The app requests only the `drive.appdata` scope plus basic identity scopes.

Before building the APK:

1. In Google Cloud Console, create a project and enable the Google Drive API. Configure the OAuth consent screen / Google Auth Platform.
2. Create a **Web application OAuth client ID** and replace `YOUR_GOOGLE_WEB_CLIENT_ID.apps.googleusercontent.com` in `www/index.html` with that value. Do not put a client secret in the app.
3. Create an **Android OAuth client** with package name `com.finora.finance` and the SHA-1 certificate fingerprint used to sign the APK. For GitHub Actions debug APKs, obtain the debug keystore SHA-1 from a locally generated Android debug keystore or use Android Studio/Gradle signing report for the same build configuration. Add each signing certificate fingerprint you use.
4. Build a new APK and install it. Google sign-in will not work in the older APK.

### Sync behaviour and limitations

- Drive backups are stored in the signed-in account's private `appDataFolder`, not in a visible user folder.
- Connect / Switch Google account to select a different Google account. Each account has a separate ledger.
- Automatic upload is attempted after a record is saved while a valid Google access token is available. Access tokens expire; when that happens, reconnect the account to authorize again. This starter implementation does not provide background sync while the app is closed.
- When a newer cloud backup is detected, FINORA asks before replacing local data. Avoid editing the same account's data on two devices simultaneously until conflict-safe merge support is added.
- Keep manual JSON backups too. This integration is a first implementation and has not yet been verified against a real Google OAuth project or a physical Android device.
