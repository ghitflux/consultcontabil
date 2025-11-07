"use client";

import { Card, CardBody, Button, Spinner, Chip, Table, TableHeader, TableColumn, TableBody, TableRow, TableCell } from "@/heroui";
import { useEffect, useState } from "react";
import { financeApi } from "@/lib/api/endpoints/finance";
import type { Transaction } from "@/types/finance";
import { formatCurrency, getPaymentStatusLabel, getPaymentStatusColor } from "@/types/finance";

export default function TransacoesPage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTransactions();
  }, []);

  const loadTransactions = async () => {
    try {
      setLoading(true);
      const data = await (financeApi as any).list({ size: 50 });
      setTransactions(data.items);
    } catch (error) {
      console.error("Error loading transactions:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Transações Financeiras</h1>
          <p className="text-default-500 mt-1">Gerencie todas as transações</p>
        </div>
        <Button color="primary">Nova Transação</Button>
      </div>

      <Card>
        <CardBody>
          <Table aria-label="Transactions table">
            <TableHeader>
              <TableColumn>CLIENTE</TableColumn>
              <TableColumn>DESCRIÇÃO</TableColumn>
              <TableColumn>VALOR</TableColumn>
              <TableColumn>VENCIMENTO</TableColumn>
              <TableColumn>STATUS</TableColumn>
            </TableHeader>
            <TableBody>
              {transactions.map((transaction) => (
                <TableRow key={transaction.id}>
                  <TableCell>{transaction.client_name || 'N/A'}</TableCell>
                  <TableCell>{transaction.description}</TableCell>
                  <TableCell>{formatCurrency(transaction.amount)}</TableCell>
                  <TableCell>{new Date(transaction.due_date).toLocaleDateString('pt-BR')}</TableCell>
                  <TableCell>
                    <Chip color={getPaymentStatusColor(transaction.payment_status)} size="sm" variant="flat">
                      {getPaymentStatusLabel(transaction.payment_status)}
                    </Chip>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardBody>
      </Card>
    </div>
  );
}
