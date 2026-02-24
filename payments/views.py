from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse
from .lnbits import create_invoice, get_wallet_details, check_invoice

class PosView(View):
    template_name = "payments/pos.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "invoice": None,
            "wallet": None,
        }
        try:
            context["wallet"] = get_wallet_details()
        except Exception:
            context["wallet_error"] = "Impossible de récupérer les infos du wallet LNbits."
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest) -> HttpResponse:
        amount = request.POST.get("amount")
        memo = request.POST.get("memo", "")
        context = {
            "invoice": None,
            "wallet": None,
        }
        try:
            context["wallet"] = get_wallet_details()
        except Exception:
            context["wallet_error"] = "Impossible de récupérer les infos du wallet LNbits."

        try:
            amount_sats = int(amount)
            if amount_sats <= 0:
                raise ValueError
        except Exception:
            context["error"] = "Montant invalide."
            return render(request, self.template_name, context)

        try:
            invoice = create_invoice(amount_sats, memo=memo)
            context["invoice"] = invoice
        except Exception as e:
            context["error"] = f"Erreur création invoice LNbits: {e}"

        return render(request, self.template_name, context)
