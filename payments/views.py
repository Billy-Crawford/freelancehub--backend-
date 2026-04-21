# payments/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from missions.models import Mission
from payments.models import Payment


class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, mission_id):
        mission = get_object_or_404(Mission, id=mission_id)

        if request.user != mission.client:
            return Response({"error": "Non autorisé"}, status=403)

        if mission.status != "in_progress":
            return Response({"error": "Mission pas en cours"}, status=400)

        app = mission.applications.filter(status="accepted").first()

        if not app:
            return Response({"error": "Aucun freelance accepté"}, status=400)

        payment, created = Payment.objects.get_or_create(
            mission=mission,
            defaults={
                "client": request.user,
                "freelancer": app.freelancer,
                "amount": mission.budget,
                "status": "held"
            }
        )

        if not created:
            return Response({"error": "Paiement déjà initié"}, status=400)

        return Response({"message": "Paiement initié"})


class ReleasePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, mission_id):
        payment = get_object_or_404(Payment, mission_id=mission_id)

        if request.user != payment.client:
            return Response({"error": "Non autorisé"}, status=403)

        if payment.status != "held":
            return Response({"error": "Paiement invalide"}, status=400)

        payment.status = "released"
        payment.save()

        payment.mission.status = "completed"
        payment.mission.save()

        return Response({"message": "Paiement envoyé"})


class CancelPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, mission_id):
        payment = get_object_or_404(Payment, mission_id=mission_id)

        if request.user != payment.client:
            return Response({"error": "Non autorisé"}, status=403)

        if payment.status == "released":
            return Response({"error": "Impossible d'annuler"}, status=400)

        payment.delete()

        return Response({"message": "Paiement annulé"})

class MyPaymentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == "client":
            payments = Payment.objects.filter(client=user)
        else:
            payments = Payment.objects.filter(freelancer=user)

        data = []
        for p in payments:
            data.append({
                "id": p.id,
                "mission_id": p.mission.id,
                "mission_title": p.mission.title,
                "amount": float(p.amount),
                "status": p.status,
            })

        return Response(data)
