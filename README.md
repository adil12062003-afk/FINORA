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
