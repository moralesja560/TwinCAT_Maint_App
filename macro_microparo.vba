Sub analysis()

arr1 = ActiveSheet.Range("current").Value

Range("i1").Select

conteo = 0

For c = 1 To UBound(arr1)
    If arr1(c, 1) = 0 Then
        conteo = conteo + 1
    ElseIf conteo > 0 Then
         ActiveCell.Value = conteo
         DoEvents
        ActiveCell.Offset(1, 0).Select
        conteo = 0
    End If
Next

ActiveCell.Offset(1, 0).Select
ActiveCell.Value = conteo

End Sub
