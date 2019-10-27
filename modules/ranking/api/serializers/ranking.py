from rest_framework import serializers


class RankingSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField(max_length=32)
    value = serializers.FloatField()
    row_number = serializers.IntegerField()

    class Meta:
        fields = ('user_id', 'username', 'value', 'row_number')


class MPRankingSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField(max_length=32)
    annotated_documents = serializers.IntegerField()
    high_agreement_percentage = serializers.FloatField()
    value = serializers.FloatField()
    row_number = serializers.IntegerField()

    class Meta:
        fields = ('user_id', 'username', 'annotated_documents', 'high_agreement_percentage', 'value', 'row_number')

